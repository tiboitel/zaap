"""Pydantic models for request/response validation."""

from pydantic import BaseModel


class AuthRequest(BaseModel):
    account_id: str
    hash_password: str


class AuthResponse(BaseModel):
    zaap_token: str


class ErrorResponse(BaseModel):
    error: str