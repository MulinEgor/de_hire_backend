"""Модуль для хранения состояний бота."""

from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    """Состояния пользователя."""

    adding_wallet = State()
    selecting_role = State()
