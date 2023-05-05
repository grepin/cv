from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    AUTH_POSTGRES_HOST: str
    AUTH_POSTGRES_PORT: int
    AUTH_POSTGRES_DB: str
    AUTH_POSTGRES_USER: str
    AUTH_POSTGRES_PASSWORD: str
    JWT_KEY: str
    EXTERNAL_PAY_API_URL: str
    INTERNAL_PAY_API_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
