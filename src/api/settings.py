"""Настройки конфигурации основного API."""

import os
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "..",
    ".env",
)


class APISettings(BaseSettings):
    """Класс переменных окружения основного API."""

    MODE: Literal["DEV", "TEST", "PROD"]
    APP_VERSION: str = "0.1.0"

    # Security
    CORS_ORIGINS: list[str]

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, extra="ignore")


settings = APISettings()
