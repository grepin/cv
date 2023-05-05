import redis

from auth.core.config import (
    REDIS_ACCESS_TOKENS_DB,
    REDIS_HOST,
    REDIS_PASSWORD,
    REDIS_PORT,
    REDIS_REFRESH_TOKENS_DB,
    REDIS_RATE_LIMITER_DB,

)

redis4rate_limiter = redis.ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=REDIS_RATE_LIMITER_DB,
)

redis4access = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=REDIS_ACCESS_TOKENS_DB)

redis4refresh = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=REDIS_REFRESH_TOKENS_DB)
