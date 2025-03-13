"""Настройки конфигурации бота."""

import os

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "..",
    ".env",
)


class BotSettings(BaseSettings):
    """Класс переменных окружения бота."""

    bot_token: str

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, extra="ignore")


settings = BotSettings()
