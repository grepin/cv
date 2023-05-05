from http import HTTPStatus

import pytest

from tests.auth.functional.settings import JWT_SECRET_KEY
from tests.auth.functional.testdata.user import USER
from tests.auth.functional.utils import (get_auth_header, get_redis_token_key,
                                         get_token_data)

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("user,http_get", [(USER[0], True), (USER[0], False)])
async def test_refresh(user, http_get, user_cleanup, user_register,
                       user_auth_tokens, user_refresh, redis_get):
    """Работает ли вызов refresh (включая корретную работу с redis)?"""
    user_cleanup(user)
    response = await user_register(user)
    assert response.status == HTTPStatus.OK
    access, refresh = await user_auth_tokens(user)
    header = get_auth_header(refresh)
    key = get_redis_token_key(get_token_data(refresh, JWT_SECRET_KEY))

    before = await redis_get(key, access=False)
    response = await user_refresh(header, http_get=http_get)
    after = await redis_get(key, access=False)

    assert response.status == HTTPStatus.OK
    assert response.body['description'] == 'tokens refreshed'
    assert 'access_token' in response.body['data']
    assert 'refresh_token' in response.body['data']
    assert before is not None
    assert after is None

    user_cleanup(user)


@pytest.mark.parametrize("user,http_get", [(USER[0], True), (USER[0], False)])
async def test_refresh_with_invalid_token(
    user,
    http_get,
    user_cleanup,
    user_register,
    user_auth_tokens,
    user_refresh
):
    """Можно ли сделать refresh с access-токеном?"""
    user_cleanup(user)
    response = await user_register(user)
    assert response.status == HTTPStatus.OK
    access, refresh = await user_auth_tokens(user)
    header = get_auth_header(access)

    response = await user_refresh(header, http_get=http_get)

    assert response.status == 457
    assert response.body['description'] == 'refresh token needed'

    user_cleanup(user)
