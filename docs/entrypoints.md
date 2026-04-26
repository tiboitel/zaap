# Entrypoints

All exposed API and runtime entry points.

## Backend Routes

| Endpoint | Method | Auth required | Description |
|----------|--------|----------------|-------------|
| `/generateAuthToken` | POST | No | Validate credentials, return token |
| `/health` | GET | No | Health check |

## Runtime Entrypoint

- **Uvicorn** — `uvicorn app.main:app --host 0.0.0.0 --port 8000`
- **Docker** — `docker compose up --build` starts `zaap`; MariaDB must be running externally on `127.0.0.1:3306`