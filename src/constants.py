"""Модуль для констант."""

from sqlalchemy import TextClause, text

from src.settings import settings

# MARK: Security
AUTH_HEADER_NAME: str = "X-Authorization"
ALGORITHM: str = "HS256"

CORS_HEADERS: list[str] = [
    "Content-Type",
    "Set-Cookie",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Origin",
    "X-Authorization",
]
CORS_METHODS: list[str] = [
    "GET",
    "POST",
    "OPTIONS",
    "DELETE",
    "PATCH",
    "PUT",
]

# MARK: Database
DB_NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
CURRENT_TIMESTAMP_UTC: TextClause = text("(CURRENT_TIMESTAMP AT TIME ZONE 'UTC')")
DEFAULT_QUERY_OFFSET: int = 0
DEFAULT_QUERY_LIMIT: int = 100

# MARK: Ethereum
WEBSOCKET_URL: str = f"wss://sepolia.infura.io/ws/v3/{settings.INFURA_PROJECT_ID}"
ABI_URL: str = f"https://api-sepolia.etherscan.io/api?module=contract&action=getabi&address={settings.CONTRACT_ADDRESS}&apikey={settings.ETHERSCAN_API_KEY}"
