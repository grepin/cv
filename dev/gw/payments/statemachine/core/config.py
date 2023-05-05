import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    RMQ_HOST: str = '127.0.0.1'
    RMQ_USER: str = 'guest'
    RMQ_PASSWORD: str = 'guest'
    RMQ_PAYMENTS_EXCHANGE: str = 'aqm.direct'
    RMQ_PAYMENTS_ROUTING_KEY: str = 'payments'
    RMQ_PAYMENTS_QUEUE: str = 'payments'

    CELERY_REDIS_HOST: str = 'celery-redis'
    CELERY_REDIS_PORT: int = 6379
    CELERY_REDIS_PASSWORD: str
    CELERY_REDIS_PAYMENTS_DB: int = 6

    AUTH_POSTGRES_DB: str = 'auth'
    AUTH_POSTGRES_USER: str = 'app'
    AUTH_POSTGRES_PASSWORD: str
    AUTH_POSTGRES_HOST: str = 'authpostgres'
    AUTH_POSTGRES_PORT: int = 5432

    CLOUDPAYMENTS_API_KEY: str
    CLOUDPAYMENTS_PUBLIC_ID: str

    LOGGING: dict = LOGGING

    class Config:
        env_file = '.env'


settings = Settings()
