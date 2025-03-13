"""Модуль для временного хранения информации о пользователях."""

from pydantic import BaseModel

from src.core.ratings import Role


class UserData(BaseModel):
    """Класс для временного хранения информации о пользователях."""

    role: Role | None = None
    wallet_address: str | None = None


user_id_to_data: dict[int, UserData] = {}
