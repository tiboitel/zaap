"""Tests for API endpoints."""

from fastapi.testclient import TestClient

from app.main import app


class TestHealthEndpoint:
    def test_health_returns_ok(self):
        client = TestClient(app)
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestGenerateAuthTokenEndpoint:
    def test_missing_account_id_returns_422(self):
        client = TestClient(app)
        response = client.post("/generateAuthToken", json={})

        assert response.status_code == 422

    def test_invalid_credentials_returns_401(self, mocker):
        mocker.patch("app.db.get_account_by_name", return_value=None)

        client = TestClient(app)
        response = client.post(
            "/generateAuthToken",
            json={"account_id": "nonexistent", "hash_password": "wrong"},
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    def test_successful_auth_returns_token(self, mocker):
        mock_account = {
            "guid": 123,
            "account": "testuser",
            "pass": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
            "zaap_token": None,
        }
        mocker.patch("app.db.get_account_by_name", return_value=mock_account)
        mocker.patch("app.db.update_zaap_token")

        client = TestClient(app)
        response = client.post(
            "/generateAuthToken",
            json={"account_id": "testuser", "hash_password": "password"},
        )

        assert response.status_code == 200
        assert "zaap_token" in response.json()
