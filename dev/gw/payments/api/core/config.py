import os
from logging import config as logging_config
from pathlib import Path

from core.logger import LOGGING
from pydantic import BaseSettings

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    RMQ_HOST: str = '127.0.0.1'
    RMQ_USER: str = 'guest'
    RMQ_PASSWORD: str = 'guest'
    RMQ_PAYMENTS_EXCHANGE: str = 'aqm.direct'
    RMQ_PAYMENTS_ROUTING_KEY: str = 'payments'
    TEMPLATES_DIR: str = os.path.join(Path(__file__).parent.parent, "templates")
    LOGGING: dict = LOGGING

    class Config:
        env_file = '.env'


settings = Settings()
