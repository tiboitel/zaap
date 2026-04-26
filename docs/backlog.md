# Backlog

Ordered task list for this project.

## Hardening (non-blocking)

| Priority | Task | Depends on |
|----------|------|------------|
| 1 | Consider Redis-backed rate limiting for multi-instance deployment | — |
| 2 | Add Redis service to compose as optional external dependency | 1 |

## Shipped

| Task |
|------|
| Fix Docker build order (source before pip install) |
| Fix Dockerfile package layout (app/ copy order) |
| Add non-root runtime user in Dockerfile |
| Install curl for healthcheck |
| Add container healthcheck |
| Harden auth logging (remove hash metadata, account identity) |
| Add rate limiting (in-memory, per-IP + per-account) |
| Remove bundled DB from compose (external MariaDB) |
| Remove weak MySQL root password fallback |
| Ignore generated files (zaap.egg-info/, OpenCode docs) |
| Document TLS requirement for /generateAuthToken |
| Document external MariaDB dependency in architecture |
| Update docs to match current deployment |
| Add integration tests for auth and rate limit paths |