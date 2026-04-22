"""Configuration loader from .env."""

from os import getenv
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

HOST = getenv("MYSQL_HOST", "127.0.0.1")
PORT = int(getenv("MYSQL_PORT", "3306"))
DATABASE = getenv("MYSQL_DATABASE", "starloco_login")
USER = getenv("MYSQL_USER", "root")
PASSWORD = getenv("MYSQL_PASSWORD", "")

API_HOST = getenv("API_HOST", "0.0.0.0")
API_PORT = int(getenv("API_PORT", "8000"))