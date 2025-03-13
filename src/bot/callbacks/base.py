"""Модуль для обработки колбэков бота."""

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.bot.keyboards import get_role_keyboard
from src.bot.states import UserStates
from src.bot.user_storage import UserData, user_id_to_data

router = Router()


@router.message(UserStates.adding_wallet)
async def process_wallet_address(message: Message, state: FSMContext):
    """Колбэк после ввода адреса кошелька пользователем."""

    wallet_address = message.text.strip()
    # Простая проверка формата Ethereum адреса
    if len(wallet_address) == 42 and wallet_address.startswith("0x"):
        # Если к пользователю не привязаны данные, то после ввода адреса кошелька,
        # то ему еще нужно выбрать роль.
        if not user_id_to_data.get(message.from_user.id):
            user_id_to_data[message.from_user.id] = UserData()
            user_id_to_data[message.from_user.id].wallet_address = wallet_address
            await message.answer(f"Ваш кошелек успешно привязан: {wallet_address}")

            await state.set_state(UserStates.selecting_role)
            await message.answer("Выберите роль:", reply_markup=get_role_keyboard())

        else:
            user_id_to_data[message.from_user.id].wallet_address = wallet_address
            await message.answer(f"Ваш кошелек успешно привязан: {wallet_address}")

    else:
        await message.answer(
            "Неверный формат адреса. Пожалуйста, введите корректный Ethereum адрес."
        )


@router.callback_query(UserStates.selecting_role)
async def process_role_selection(callback: CallbackQuery):
    """Колбэк после выбора роли пользователем."""

    role = callback.data.split(":")[1]
    user_id_to_data[callback.from_user.id].role = role
    await callback.message.answer("Вы успешно выбрали роль.")
