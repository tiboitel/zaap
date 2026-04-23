"""Database layer using SQLAlchemy."""

import logging
from urllib.parse import quote_plus

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, Session

from app import config

logger = logging.getLogger(__name__)

_engine = None
_SessionLocal = None


def get_engine():
    global _engine
    if _engine is None:
        url = URL.create(
            drivername="mysql+pymysql",
            username=quote_plus(config.USER),
            password=config.PASSWORD,
            host=config.HOST,
            port=config.PORT,
            database=config.DATABASE,
        )
        logger.info("Connecting to DB: %s:%s/%s", config.HOST, config.PORT, config.DATABASE)
        _engine = create_engine(url, pool_pre_ping=True)
    return _engine


def get_session() -> Session:
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=get_engine())
    return _SessionLocal()


def get_account_by_name(account_id: str) -> dict | None:
    """Fetch account by account name only."""
    session = get_session()
    try:
        query = text("""
            SELECT guid, account AS user, pass AS pwd, zaap_token AS token
            FROM world_accounts
            WHERE account = :account
            LIMIT 1
        """)
        logger.debug("Query: account=%s", account_id)
        result = session.execute(query, {"account": account_id})
        row = result.fetchone()
        if row:
            logger.info("Account found: guid=%d, user=%s", row.guid, row.user)
            return {
                "guid": row.guid,
                "account": row.user,
                "pass": row.pwd,
                "zaap_token": row.token,
            }
        logger.warning("No account found for: %s", account_id)
        return None
    except Exception as e:
        logger.error("DB error: %s", e)
        raise
    finally:
        session.close()


def update_zaap_token(guid: int, token: str) -> None:
    """Update zaap_token for a given guid."""
    session = get_session()
    try:
        query = text("""
            UPDATE world_accounts
            SET zaap_token = :token
            WHERE guid = :guid
        """)
        session.execute(query, {"token": token, "guid": guid})
        session.commit()
        logger.info("Token updated for guid=%d", guid)
    except Exception as e:
        logger.error("Failed to update token: %s", e)
        raise
    finally:
        session.close()