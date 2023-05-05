from http import HTTPStatus

import pytest

from tests.auth.functional.testdata.user import MISSING_FIELD_USERS, USER

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("user", USER)
async def test_register_first_time(user, user_cleanup, user_register):
    """Работает ли вызов register?"""
    user_cleanup(user)

    response = await user_register(user)

    assert response.status == HTTPStatus.OK
    assert response.body['description'] == 'user registered'
    assert 'password' not in response.body['data']
    assert 'id' in response.body['data']
    assert response.body['data']['login'] == user['login']
    assert response.body['data']['active'] == 1
    assert 'user' in response.body['data']['roles']

    user_cleanup(user)


@pytest.mark.parametrize("user", USER)
async def test_register_twice(user, user_cleanup, user_register):
    """Поведение вызова register при дублирующих данных"""
    user_cleanup(user)

    await user_register(user)
    response = await user_register(user)

    assert response.status == 451
    assert response.body['description'] == 'constraints validation error'
    assert 'already exists' in response.body['data'].values()

    user_cleanup(user)


@pytest.mark.parametrize("user", MISSING_FIELD_USERS)
async def test_register_missing(user, user_register):
    """Провека попытки регистрации с нехваткой обязательных данных"""
    response = await user_register(user)

    assert response.status == 452
    assert response.body['description'] == 'input validation error'
    assert 'Missing data for required field' in str(response.body['data'])
