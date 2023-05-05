from http import HTTPStatus

import pytest

from tests.auth.functional.testdata.user import USER

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("user", USER)
async def test_login(user, user_cleanup, user_register, user_login):
    """Работает ли вызов login для зарегистрированного пользователя?"""
    user_cleanup(user)
    response = await user_register(user)
    assert response.status == HTTPStatus.OK

    response = await user_login(user)

    assert response.status == HTTPStatus.OK
    assert 'access_token' in response.body['data']
    assert 'refresh_token' in response.body['data']
    assert response.body['description'] == 'authenticated successfully'
    assert 'id' in response.body['data']
    assert 'password' not in response.body['data']
    assert response.body['data']['login'] == user['login']
    assert response.body['data']['active'] == 1
    assert 'roles' in response.body['data']

    user_cleanup(user)


@pytest.mark.parametrize("user", USER)
async def test_login_non_existing(user, user_login, random_string, user_cleanup):
    """Возможно ли зайти с несуществующим аккаунтом?"""
    user_cleanup(user)
    user['login'] = random_string(8)

    response = await user_login(user)

    assert response.body['description'] == 'no such user'
    assert response.status == 450

    user_cleanup(user)


@pytest.mark.parametrize("user", USER)
async def test_login_wrong_password(user, user_cleanup, user_register, user_login, random_string):
    """Возможно ли зайти с неверным паролем?"""
    user_cleanup(user)
    response = await user_register(user)
    assert response.status == HTTPStatus.OK
    user['password'] = random_string(12)

    response = await user_login(user)

    assert response.body['data'] == {}
    assert response.status == 441
    assert response.body['description'] == 'invalid credentials'

    user_cleanup(user)
