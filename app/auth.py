"""Authentication logic."""

import logging
import secrets

from app import db
from app.schemas import AuthRequest, AuthResponse, ErrorResponse

logger = logging.getLogger(__name__)


def generate_token() -> str:
    """Generate a 36-character token."""
    return secrets.token_hex(18)


def authenticate(
    request: AuthRequest,
) -> tuple[AuthResponse, int] | tuple[ErrorResponse, int]:
    """Authenticate and return token or error."""
    logger.info("Auth attempt for account=%s", request.account_id)

    account = db.get_account_by_name(request.account_id)
    if account is None:
        logger.warning("Account not found: %s", request.account_id)
        return ErrorResponse(error="Invalid credentials"), 401

    stored_hash = account["pass"]
    input_hash = request.password_hash
    stored_len = len(stored_hash) if stored_hash else 0
    input_len = len(input_hash)

    logger.info("Password check: stored_len=%d, input_len=%d", stored_len, input_len)
    logger.debug(
        "Debug hashes: stored_prefix=%s..., input_prefix=%s...",
        stored_hash[:16] if stored_hash else "None",
        input_hash[:16],
    )

    if stored_hash != input_hash:
        logger.warning(
            "Password mismatch for: %s (lengths: stored=%d, computed=%d)",
            request.account_id,
            stored_len,
            input_len,
        )
        return ErrorResponse(error="Invalid credentials"), 401

    token = generate_token()
    db.update_zaap_token(account["guid"], token)

    logger.info("Auth success for: %s", request.account_id)
    return AuthResponse(zaap_token=token), 200
