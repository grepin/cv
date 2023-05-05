from pyrate_limiter import Duration, RequestRate, Limiter, RedisBucket
from redis import ConnectionPool
from flask import Flask, request, has_request_context
from auth.utils.http_exceptions import RateLimitExceeded
from auth.core.config import (
    RATE_LIMITER_REQUESTS_PER_SECOND,
    RATE_LIMITER_REQUESTS_PER_MINUTE,
)

import re


def rate_limit_identity():
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    ua = request.environ.get('HTTP_USER_AGENT', '_')
    return '{}_{}'.format(ip, ua)


def init_rate_limiter(redis_pool: ConnectionPool, app: Flask):
    rate_limiter = Limiter(
        RequestRate(RATE_LIMITER_REQUESTS_PER_SECOND, Duration.SECOND),
        RequestRate(RATE_LIMITER_REQUESTS_PER_MINUTE, Duration.MINUTE),
        bucket_class=RedisBucket,
        bucket_kwargs={'redis_pool': redis_pool, 'bucket_name': 'RL'},
    )

    def apply_rate_limit():
        try:
            if has_request_context():
                if len(re.findall('openapi|flasgger', request.environ['PATH_INFO'])) == 0:
                    rate_limiter.try_acquire(rate_limit_identity())
        except Exception:
            raise RateLimitExceeded()
    app.execute_before_request.append(apply_rate_limit)

    return rate_limiter
