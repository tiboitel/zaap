# Zaap

FastAPI-based auth backend for Starloco Zaap service.

## Overview

Zaap exposes a small authentication API backed by MySQL. It validates legacy password hashes, generates a `zaap_token`, and stores it in `world_accounts`.

## Requirements

- Python 3.10+
- MySQL database with access to `world_accounts`

## Setup

```bash
pip install -e ".[dev]"
```

Copy `.env.example` to `.env` and configure:

```env
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=starloco_login
MYSQL_USER=root
MYSQL_PASSWORD=

API_HOST=0.0.0.0
API_PORT=8000
```

## Run

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Or with Docker:

```bash
docker compose up --build
```

## Endpoints

- `GET /health` — Health check
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

## Testing

```bash
pytest
```

## Notes

- Client must hash password before sending: `SHA512(MD5(password))`
- Plain password must never be transmitted over the network
- Database credentials are URL-safe in `app/db.py`
- `.env` files and Python caches are ignored by git