# Zaap

FastAPI-based auth backend for Starloco Zaap service.

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
zaap
```

Or directly with uvicorn:

```bash
uvicorn app.main:app --reload
```

## Endpoints

- `GET /health` — Health check
- `POST /generateAuthToken` — Generate auth token