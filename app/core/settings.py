import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from pathlib import Path


# Определение пути к корню проекта
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Выбор env-файла в зависимости от окружения
env_name = os.getenv("ENV", "dev")


if env_name == "test":
    load_dotenv(BASE_DIR / ".env.test")
else:
    load_dotenv(BASE_DIR / ".env")


class Settings(BaseSettings):

    # Основные настройки
    ENV: str = env_name
    DEBUG: bool = True

    # База данных
    DATABASE_URL: str

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int = 0
    CRYPTO_PRICE_TTL_SECONDS: int = 60
    CRYPTO_LIST_TTL_MINUTES: int = 60

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_TTL_MINUTES: int = 30
    REFRESH_TOKEN_TTL_DAYS: int = 30

    # Ключ API CoinMarketCap
    API_KEY: str

    # Конфиг настроек
    model_config = SettingsConfigDict(case_sensitive=True)


settings = Settings()