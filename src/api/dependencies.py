"""Зависимости эндпоинтов API."""

from typing import AsyncGenerator

from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.constants import AUTH_HEADER_NAME
from src.core.database import SessionLocal

oauth2_scheme = APIKeyHeader(name=AUTH_HEADER_NAME, auto_error=False)


# MARK: Database
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    AsyncGenerator экземпляра `AsyncSession`.

    Выполняет `rollback` текущей транзакции, в случае любого исключения.
    Сессия закрывается внутри контекстного менеджера автоматически.

    **Коммит транзакции должен быть выполнен явно.**
    """

    async with SessionLocal() as session:
        try:
            yield session
        except Exception as ex:
            await session.rollback()
            raise ex
