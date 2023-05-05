from http import HTTPStatus

import pytest

from tests.auth.functional.testdata.user import USER

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("user", USER)
async def test_update_no_token(user, user_update):
    """Провека попытки обновления данных без токена авторизации"""
    response = await user_update({}, user)
    assert response.status == 440


@pytest.mark.parametrize("user", USER)
async def test_update(user, user_cleanup, user_register, user_auth_access_header, user_update, random_string):
    """Провека корректной попытки обновления данных"""
    copy = user.copy()
    user_cleanup(user)
    user_cleanup(copy)
    response = await user_register(user)
    assert response.status == HTTPStatus.OK
    auth_headers = await user_auth_access_header(user)
    user['login'] = random_string(6)
    user['name'] = random_string(12)
    user['email'] = random_string(8) + '@mankind.com'
    user['password'] = random_string(8)

    response = await user_update(auth_headers, user)

    assert response.status == HTTPStatus.OK
    assert response.body['description'] == 'user updated'
    assert response.body['data']['login'] == user['login']
    assert response.body['data']['email'] == user['email']
    assert response.body['data']['name'] == user['name']

    user_cleanup(copy)
    user_cleanup(user)
