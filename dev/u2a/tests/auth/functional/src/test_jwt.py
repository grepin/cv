from http import HTTPStatus

import pytest

from tests.auth.functional.settings import JWT_SECRET_KEY
from tests.auth.functional.testdata.user import USER
from tests.auth.functional.utils import (get_auth_header, get_redis_token_key,
                                         get_token_data)

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("user", USER)
async def test_refresh_token_in_redis(user, user_cleanup, user_register, user_auth_tokens, redis_get):
    """Помещен ли выданный refresh-токен в redis?"""
    user_cleanup(user)
    response = await user_register(user)
    assert response.status == HTTPStatus.OK
    access, refresh = await user_auth_tokens(user)
    key = get_redis_token_key(get_token_data(refresh, JWT_SECRET_KEY))

    status = await redis_get(key, access=False)

    assert status is not None

    user_cleanup(user)


@pytest.mark.parametrize("user", USER)
async def test_invalidate_access_token(user, user_cleanup, user_register, user_auth_tokens, redis_set, user_update):
    """Работет ли механизм инвалидации access-токенов через redis?"""
    user_cleanup(user)
    response = await user_register(user)
    assert response.status == HTTPStatus.OK
    access, refresh = await user_auth_tokens(user)
    key = get_redis_token_key(get_token_data(access, JWT_SECRET_KEY))

    await redis_set(key, 0)
    response = await user_update(get_auth_header(access), {})

    assert response.body['description'] == 'access token revoked'
    assert response.status == 456

    user_cleanup(user)
