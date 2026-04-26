# Architecture

System boundaries, startup order, data flow.

## Overview

Starloco Zaap is an authentication service. It exposes a single token-generation endpoint for legacy game account login. Clients send credentials; the service validates them against the MariaDB database and returns a token.

## Components

- **FastAPI app** — HTTP endpoints, request validation
- **Auth logic** — credential verification, token generation
- **Database layer** — MariaDB access, account lookup and token persistence
- **Config loader** — environment variable loading from `.env`

## Startup Order

> **Startup order:** mariadb → backend

The backend depends on an external MariaDB instance running on `127.0.0.1:3306`. Ensure MariaDB is running and reachable before starting the API.

If the API fails to start or returns connection errors, confirm MariaDB is healthy and accessible.

## Data Flow

1. Client POSTs to `/generateAuthToken` with `{ account_id, password_hash }`
2. FastAPI validates the request schema
3. `authenticate()` looks up the account in `world_accounts` table
4. Plaintext hash comparison (no hashing applied server-side)
5. On success: generate token, persist to `zaap_token` column
6. Return token in response

**Network boundary:** API listens on `0.0.0.0:8000`. MariaDB is external on `127.0.0.1:3306`.

## Constraints

- Database schema is read-only. Do not modify `world_accounts` structure.
- Vendor and submodules must not be touched.
- **/generateAuthToken must be served over HTTPS.** This endpoint accepts password-equivalent material (password_hash) which is replayable over plain HTTP. Deploy behind a reverse proxy or TLS terminator before production use.