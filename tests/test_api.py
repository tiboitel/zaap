"""Integration tests for auth endpoint and rate limiting."""

from fastapi.testclient import TestClient
import pytest

from app.main import app, auth_limiter


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def correct_hash():
    return "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"


@pytest.fixture
def mock_account(correct_hash):
    return {
        "guid": 123,
        "account": "testuser",
        "pass": correct_hash,
        "zaap_token": None,
    }


class TestHealthEndpoint:
    def test_health_returns_ok(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestGenerateAuthTokenEndpoint:
    def test_missing_account_id_returns_422(self, client):
        response = client.post("/generateAuthToken", json={})
        assert response.status_code == 422

    def test_invalid_credentials_returns_401(self, client, mocker):
        mocker.patch("app.db.get_account_by_name", return_value=None)
        response = client.post(
            "/generateAuthToken",
            json={"account_id": "nonexistent", "password_hash": "wrong"},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    def test_successful_auth_returns_token(self, client, mocker, mock_account):
        mocker.patch("app.db.get_account_by_name", return_value=mock_account)
        update_mock = mocker.patch("app.db.update_zaap_token")
        response = client.post(
            "/generateAuthToken",
            json={"account_id": "testuser", "password_hash": mock_account["pass"]},
        )
        assert response.status_code == 200
        assert "zaap_token" in response.json()
        update_mock.assert_called_once()


class TestGenerateAuthTokenRateLimit:
    @pytest.fixture(autouse=True)
    def reset_rate_limiter(self):
        auth_limiter._ip_timestamps.clear()
        auth_limiter._account_timestamps.clear()
        yield
        auth_limiter._ip_timestamps.clear()
        auth_limiter._account_timestamps.clear()

    def test_rate_limit_by_ip_returns_429(self, client, mocker, mock_account):
        mocker.patch("app.db.get_account_by_name", return_value=mock_account)
        mocker.patch("app.db.update_zaap_token")
        for _ in range(12):
            response = client.post(
                "/generateAuthToken",
                json={"account_id": f"user_{_}", "password_hash": mock_account["pass"]},
            )
            assert response.status_code == 200
        response = client.post(
            "/generateAuthToken",
            json={"account_id": "user_overflow", "password_hash": mock_account["pass"]},
        )
        assert response.status_code == 429
        assert response.json()["detail"] == "Too many attempts"
        assert "retry_after_seconds" in response.json()
        assert response.headers.get("Retry-After")

    def test_rate_limit_by_account_returns_429(self, client, mocker, mock_account):
        mocker.patch("app.db.get_account_by_name", return_value=mock_account)
        mocker.patch("app.db.update_zaap_token")
        for _ in range(6):
            response = client.post(
                "/generateAuthToken",
                json={"account_id": "testuser", "password_hash": mock_account["pass"]},
            )
            assert response.status_code == 200
        response = client.post(
            "/generateAuthToken",
            json={"account_id": "testuser", "password_hash": mock_account["pass"]},
        )
        assert response.status_code == 429
        assert response.json()["detail"] == "Too many attempts"
        assert "retry_after_seconds" in response.json()
        assert response.headers.get("Retry-After")

    def test_retry_after_consistency(self, client, mocker, mock_account):
        mocker.patch("app.db.get_account_by_name", return_value=mock_account)
        mocker.patch("app.db.update_zaap_token")
        for _ in range(12):
            client.post(
                "/generateAuthToken",
                json={"account_id": f"user_{_}", "password_hash": mock_account["pass"]},
            )
        response = client.post(
            "/generateAuthToken",
            json={"account_id": "user_overflow", "password_hash": mock_account["pass"]},
        )
        header_value = int(response.headers.get("Retry-After", "0"))
        body_value = response.json()["retry_after_seconds"]
        assert header_value == body_value