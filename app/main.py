"""FastAPI application entry point."""

import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

from app import config
from app.auth import authenticate
from app.rate_limit import RateLimitError, auth_limiter
from app.schemas import AuthRequest, AuthResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="ZaapAuth", version="1.0.0")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("%s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("%s %s -> %d", request.method, request.url.path, response.status_code)
    return response


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/generateAuthToken", response_model=AuthResponse)
async def generate_auth_token(request: AuthRequest, http_request: Request):
    try:
        auth_limiter.check(ip=http_request.client.host, account_id=request.account_id)
    except RateLimitError as e:
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Too many attempts",
                "retry_after_seconds": e.retry_after,
            },
            headers={"Retry-After": str(e.retry_after)},
        )
    logger.info("Auth attempt from %s", http_request.client.host)
    response, status_code = authenticate(request)
    if status_code == 401:
        raise HTTPException(status_code=401, detail=response.error)
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT)