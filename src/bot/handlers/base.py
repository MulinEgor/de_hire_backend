"""
Модуль для обработки команд бота (для пользователей,
которые еще не прикрепили свой кошелек и не выбрали роль)
"""

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.keyboards import get_role_keyboard
from src.bot.states import UserStates
from src.bot.user_storage import user_id_to_data

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    """Обработка команды /start."""

    data = user_id_to_data.get(message.from_user.id)
    if data is None or data.wallet_address is None:
        await state.set_state(UserStates.adding_wallet)
        await message.answer(
            "Введите адрес вашего кошелька (в сети Ethereum),\
             привязанного к вашему аккунту в @wallet:"
        )
        return

    if data.role is None:
        await state.set_state(UserStates.selecting_role)
        await message.answer("Выберите роль:", reply_markup=get_role_keyboard())
        return

    await message.answer("Вы прикрепили свой кошелек и выбрали роль.")
