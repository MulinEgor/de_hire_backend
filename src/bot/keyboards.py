"""Модуль для создания и управления клавиатурами бота."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.core.ratings.models import Role


def get_role_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора роли."""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Работник", callback_data=f"role:{Role.EMPLOYEE.value}"
        ),
        InlineKeyboardButton(
            text="Работодатель", callback_data=f"role:{Role.EMPLOYER.value}"
        ),
    )
    return builder.as_markup()
