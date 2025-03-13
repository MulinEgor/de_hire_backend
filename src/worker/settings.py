"""Настройки конфигурации воркера для собра информации с блокчейна."""

import os

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE_PATH = os.path.join("app", ".env")


class WorkerSettings(BaseSettings):
    """Класс переменных окружения воркера для собра информации с блокчейна."""

    INFURA_PROJECT_ID: str
    ETHERSCAN_API_KEY: str
    CONTRACT_ADDRESS: str

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH)


settings = WorkerSettings()
