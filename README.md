# Zaap

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

FastAPI-based auth backend for Starloco Zaap service.

## Key Features

- FastAPI-based REST API for legacy authentication
- Validates SHA512(MD5(password)) hashed credentials
- MariaDB backend with world_accounts token storage
- Token-based rate limiting (IP + account)
- Docker & uvicorn support

## Overview

Zaap exposes a small authentication API backed by MariaDB. It validates legacy password hashes, generates a `zaap_token`, and stores it in `world_accounts`.

## Requirements

- Python 3.10+
- MariaDB running on `127.0.0.1:3306` with access to `world_accounts`

## Setup

```bash
pip install -e ".[dev]"
```

Copy `.env.example` to `.env` and configure:

```env
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=starloco_login
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password

API_HOST=0.0.0.0
API_PORT=8000
```

Ensure MariaDB is running before starting the backend.

## Run

```bash
uvicorn app.main:app --host "${API_HOST:-0.0.0.0}" --port "${API_PORT:-8000}"
```

Or with Docker:

```bash
docker compose up --build
```

The service exposes `API_PORT` (default `8000`). Set `EXTERNAL_PORT` to change the host port mapping.

## Endpoints

- `GET /health` — Health check (no auth, no DB query)
- `POST /generateAuthToken` — Generate auth token

### `POST /generateAuthToken`

Request body:

```json
{
  "account_id": "username",
  "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
}
```

`password_hash` must be `SHA512(MD5(password))` - compute it client-side before sending.

Response:

```json
{
  "zaap_token": "generated-token"
}
```

Error responses:

- `401` — Invalid credentials
- `422` — Missing or invalid request body
- `429` — Rate limit exceeded (body includes `retry_after_seconds`, header includes `Retry-After`)

Rate limiting:

- 12 requests per minute per IP
- 6 requests per 10 minutes per account

### Rate limit response (429)

```json
{
  "detail": "Too many attempts",
  "retry_after_seconds": 42
}
```

**Important:** `/generateAuthToken` must be served over HTTPS. The endpoint accepts password-equivalent material which is replayable over plain HTTP.

## Testing

```bash
pytest
```

## Notes

- Client must hash password before sending: `SHA512(MD5(password))`
- Plain password must never be transmitted over the network
- Database credentials are URL-safe in `app/db.py`
- `.env` files and Python caches are ignored by git
- Rate limiting uses in-memory state and resets on restart or new container instance