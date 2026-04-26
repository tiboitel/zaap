# Flows

Key execution flows by domain.

## Auth Flow

| Step | Actor | Action |
|------|-------|--------|
| 1 | Client | POST `/generateAuthToken` with `{ account_id, password_hash }` |
| 2 | FastAPI | Validate request via Pydantic schema |
| 3 | Auth logic | Fetch account by name from external MariaDB |
| 4 | Auth logic | Compare password hash (plaintext comparison) |
| 5 | Auth logic | Generate 36-char token via `secrets.token_hex(18)` |
| 6 | DB layer | Write token to `world_accounts.zaap_token` |
| 7 | API | Return `{ zaap_token: <token> }` |

## Health Check

| Step | Actor | Action |
|------|-------|--------|
| 1 | Client | GET `/health` |
| 2 | FastAPI | Return `{ status: "ok" }` |

No auth required; no DB query.