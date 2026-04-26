# Conventions

Coding standards, error handling, git workflow.

## Python / FastAPI

- Follow PEP 8. Run `ruff check . && ruff format --check .` before committing.
- Use type hints on all function signatures.
- Pydantic v2 for request/response schemas.

## Error Handling

- Raise `HTTPException` with appropriate status code.
- Return 401 for auth failures; 422 for validation failures.
- Log at `INFO` for requests, `WARNING` for failures. Do not log credentials.

## Git Workflow

- Branch naming: `feature/`, `fix/`, `refactor/`
- Commit message: present tense, imperative, short subject line
- Do not commit secrets, `.env`, or local-only OpenCode files

## Startup Order

> mariadb → backend

Ensure MariaDB is running on `127.0.0.1:3306` before starting the API. The backend connects directly to the external database.