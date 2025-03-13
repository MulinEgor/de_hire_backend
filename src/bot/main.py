"""Модуль для запуска бота."""

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from src.bot.callbacks.base import router as base_callbacks_router
from src.bot.handlers.base import router as base_handlers_router
from src.bot.settings import settings


def register_handlers(dp: Dispatcher):
    """Регистрация обработчиков."""

    dp.include_router(base_handlers_router)


def register_callbacks(dp: Dispatcher):
    """Регистрация callbackов."""

    dp.include_router(base_callbacks_router)


async def main():
    """
    Точка входа бота.
    """

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация обработчиков и callbackов
    register_handlers(dp)
    register_callbacks(dp)

    print("Бот запущен")

    # Запуск бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
