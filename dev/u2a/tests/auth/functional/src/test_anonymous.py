from http import HTTPStatus

import pytest

from tests.auth.functional.testdata.user import USER
from tests.auth.functional.utils import get_auth_header

pytestmark = pytest.mark.asyncio


async def test_anon_welcome(welcome):
    """Проверка логина и получения токенов для анонимного пользователя"""

    response = await welcome()

    assert response.status == HTTPStatus.OK
    assert response.body['description'] == 'authenticated successfully'
    assert 'access_token' in response.body['data']
    assert 'refresh_token' in response.body['data']


@pytest.mark.parametrize("user", USER)
async def test_anon_welcome_tokens(user, welcome_auth_access_header_and_data, user_update):
    """Проверка неизменяемости анонима в сочетании корректным ответом"""
    auth_headers, anonymous = await welcome_auth_access_header_and_data()

    response = await user_update(auth_headers, user)

    assert response.status == HTTPStatus.OK
    assert response.body['description'] == 'user updated'
    assert response.body['data']['login'] == anonymous['login']
    assert response.body['data']['email'] == anonymous['email']
    assert response.body['data']['name'] == anonymous['name']
    assert response.body['data']['lastname'] == anonymous['name']


async def test_anon_logout(welcome_auth_access_header_and_data, user_logout):
    """Проверка бессмысленности logout для анонима при корректном ответе"""
    auth_headers, anonymous = await welcome_auth_access_header_and_data()

    await user_logout(auth_headers)
    response = await user_logout(auth_headers)

    assert response.status == HTTPStatus.OK
    assert response.body['description'] == 'logged out successfully'


async def test_anon_terminate(welcome_auth_access_header_and_data, user_terminate):
    """Проверка бессмысленности logout для анонима при корректном ответе"""
    auth_headers, anonymous = await welcome_auth_access_header_and_data()

    await user_terminate(auth_headers)
    response = await user_terminate(auth_headers)

    assert response.status == HTTPStatus.OK
    assert response.body['description'] == 'all sessions terminated'


async def test_anon_refresh(welcome_auth_tokens, user_refresh, user_terminate):
    """Проверка корректности как старых, так обновленных токенов"""
    access, refresh = await welcome_auth_tokens()
    auth_headers = get_auth_header(refresh)

    response = await user_refresh(auth_headers)
    access2, refresh2 = response.body['data']['access_token'], response.body['data']['refresh_token']
    response_access = await user_terminate(get_auth_header(access))
    response_refresh = await user_refresh(auth_headers)

    assert response_access.status == HTTPStatus.OK
    assert response_refresh.status == HTTPStatus.OK
    assert access != access2
    assert refresh != refresh2


async def test_anon_sessions(welcome_auth_access_header_and_data, user_refresh, user_sessions):
    """Анонимус должен получить пустой список сессий"""
    auth_headers, data = await welcome_auth_access_header_and_data()

    response = await user_sessions(auth_headers)

    assert response.status == HTTPStatus.OK
    assert response.body['data']['sessions'] == []
