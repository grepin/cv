import os
from logging import config as logging_config
from pathlib import Path

from dotenv import load_dotenv

from auth.core.logger import LOGGING

load_dotenv()

logging_config.dictConfig(LOGGING)

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 1))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
REDIS_ACCESS_TOKENS_DB = int(os.getenv('REDIS_ACCESS_TOKENS_DB', 2))
REDIS_REFRESH_TOKENS_DB = int(os.getenv('REDIS_REFRESH_TOKENS_DB', 3))
REDIS_RATE_LIMITER_DB = int(os.getenv('REDIS_RATE_LIMITER_DB', 4))

RATE_LIMITER_REQUESTS_PER_SECOND = int(os.getenv('RATE_LIMITER_REQUESTS_PER_SECOND', 10))
RATE_LIMITER_REQUESTS_PER_MINUTE = int(os.getenv('RATE_LIMITER_REQUESTS_PER_MINUTE', 30))
RATE_LIMITER_REQUESTS_PER_HOUR = int(os.getenv('RATE_LIMITER_REQUESTS_PER_MINUTE', 1200))

POSTGRES_USER = os.getenv('POSTGRES_USER', '')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '')
POSTGRES_DB = os.getenv('POSTGRES_DB', '')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '2eF6^D!ef_44')
JWT_ACCESS_TOKEN_EXPIRES_SECONDS = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES_SECONDS', 60))
JWT_REFRESH_TOKEN_EXPIRES_SECONDS = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES_SECONDS', 300))
JWT_FRESH_TOKEN_EXPIRES_SECONDS = int(os.getenv('JWT_FRESH_TOKEN_EXPIRES_SECONDS', 30))
JWT_ANONYMOUS_ACCESS_TOKEN_EXPIRES_SECONDS = int(os.getenv('JWT_ANONYMOUS_ACCESS_TOKEN_EXPIRES_SECONDS', 86400000))
JWT_ANONYMOUS_REFRESH_TOKEN_EXPIRES_SECONDS = int(os.getenv('JWT_ANONYMOUS_REFRESH_TOKEN_EXPIRES_SECONDS', 86400000))


SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB
)

SQLALCHEMY_TRACK_MODIFICATIONS = False

BASE_DIR = Path(__file__).parent.parent

OAUTH_CALLBACK_PREFIX = os.getenv('OAUTH_CALLBACK_PREFIX')
OAUTH_CALLBACK_POSTFIX = os.getenv('OAUTH_CALLBACK_POSTFIX')

OAUTH_YANDEX_ID = os.getenv('OAUTH_YANDEX_ID')
OAUTH_YANDEX_SECRET = os.getenv('OAUTH_YANDEX_SECRET')
OAUTH_YANDEX_URL = os.getenv('OAUTH_YANDEX_URL', 'https://oauth.yandex.ru/authorize')
OAUTH_YANDEX_TOKEN_URL = os.getenv('OAUTH_YANDEX_TOKEN_URL', 'https://oauth.yandex.ru/token')
OAUTH_YANDEX_INFO_URL = os.getenv('OAUTH_YANDEX_INFO_URL', 'https://login.yandex.ru/info')

GRPC_SERVER_PORT = int(os.getenv('GRPC_SERVER_PORT', 55005))
GRPC_SERVER_THREADS = int(os.getenv('GRPC_SERVER_THREADS', 4))
GRPC_SERVER_HOST = os.getenv('GRPC_SERVER_HOST', '127.0.0.1')

JAEGER_AGENT_HOST = os.getenv('JAEGER_AGENT_HOST', '127.0.0.1')
JAEGER_AGENT_PORT = int(os.getenv('JAEGER_AGENT_PORT', 6831))

JAEGER_REQUEST_ID_MODE = int(os.getenv('JAEGER_REQUEST_ID_MODE', 2))
