import os

from dotenv import load_dotenv

load_dotenv()

AUTH_API_HOST = os.getenv('AUTH_API_HOST', 'http://127.0.0.1:5000')
AUTH_API_PATH_V1 = os.getenv('AUTH_API_PATH_V1', '/auth/v1')

POSTGRES_USER = os.getenv('POSTGRES_USER', '')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '')
POSTGRES_DB = os.getenv('POSTGRES_DB', '')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')

SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB
)

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 1))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
REDIS_ACCESS_TOKENS_DB = int(os.getenv('REDIS_ACCESS_TOKENS_DB', 2))
REDIS_REFRESH_TOKENS_DB = int(os.getenv('REDIS_REFRESH_TOKENS_DB', 3))

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '2eF6^D!ef_44')
JWT_ACCESS_TOKEN_EXPIRES_SECONDS = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES_SECONDS', 60))
JWT_REFRESH_TOKEN_EXPIRES_SECONDS = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES_SECONDS', 300))
JWT_FRESH_TOKEN_EXPIRES_SECONDS = int(os.getenv('JWT_FRESH_TOKEN_EXPIRES_SECONDS', 30))
