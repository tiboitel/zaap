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
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Or with Docker:

```bash
docker compose up --build
```

## Endpoints

- `GET /health` — Health check
- `POST /generateAuthToken` — Generate auth token

## Testing

```bash
pytest
```