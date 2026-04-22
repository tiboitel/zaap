"""Tests for password hash logic."""

import hashlib

from app.auth import hash_password


class TestHashPassword:
    def test_hash_password_produces_sha512_of_md5(self):
        input_password = "testpassword"
        expected_md5 = hashlib.md5(input_password.encode()).hexdigest()
        expected_sha512 = hashlib.sha512(expected_md5.encode()).hexdigest()

        result = hash_password(input_password)

        assert result == expected_sha512

    def test_hash_password_is_consistent(self):
        password = "myp@ssw0rd!"

        result1 = hash_password(password)
        result2 = hash_password(password)

        assert result1 == result2

    def test_hash_password_different_inputs_produce_different_hashes(self):
        result1 = hash_password("password1")
        result2 = hash_password("password2")

        assert result1 != result2
