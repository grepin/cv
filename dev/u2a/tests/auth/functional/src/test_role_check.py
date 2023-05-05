from http import HTTPStatus

import pytest

from tests.auth.functional.testdata.role import \
    SUFFICIENT_ROLES_WITH_USER_FOR_GRANT

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("sufficient_role,checked_role,user", SUFFICIENT_ROLES_WITH_USER_FOR_GRANT)
async def test_role_check_sufficient_existing(
    sufficient_role,
    checked_role,
    user,
    user_cleanup,
    user_register,
    user_auth_access_header,
    role_assign,
    role_check,
):
    """Проверить у пользователя одну из присвоенных ролей"""
    user_cleanup(user)
    response = await user_register(user)
    user_id = response.body['data']['id']
    role_assign(user, sufficient_role)
    role_assign(user, checked_role)
    user_auth_header = await user_auth_access_header(user)
    data = {'id': user_id, 'name': checked_role}

    response = await role_check(user_auth_header, data)

    assert response.status == HTTPStatus.OK
    assert response.body['description'] == 'checked, allowed'

    user_cleanup(user)


@pytest.mark.parametrize("sufficient_role,checked_role,user", SUFFICIENT_ROLES_WITH_USER_FOR_GRANT)
async def test_role_check_sufficient_not_assigned(
    sufficient_role,
    checked_role,
    user,
    user_cleanup,
    user_register,
    user_auth_access_header,
    role_assign,
    role_check,
):
    """Проверить у пользователя одну из не присвоенных ролей"""
    user_cleanup(user)
    response = await user_register(user)
    user_id = response.body['data']['id']
    role_assign(user, sufficient_role)
    user_auth_header = await user_auth_access_header(user)
    data = {'id': user_id, 'name': checked_role}

    response = await role_check(user_auth_header, data)

    assert response.status == 461
    assert response.body['description'] == 'role was not granted to user'

    user_cleanup(user)


@pytest.mark.parametrize("sufficient_role,checked_role,user", SUFFICIENT_ROLES_WITH_USER_FOR_GRANT)
async def test_role_check_sufficient_nonex_user(
    sufficient_role,
    checked_role,
    user,
    user_cleanup,
    user_register,
    user_auth_access_header,
    role_assign,
    role_check,
):
    """Проверить роль у несуществующего пользователя"""
    user_cleanup(user)
    await user_register(user)
    user_id = '123e4567-0000-0000-0000-426614174000'
    role_assign(user, sufficient_role)
    user_auth_header = await user_auth_access_header(user)
    data = {'id': user_id, 'name': checked_role}

    response = await role_check(user_auth_header, data)

    assert response.status == 461
    assert response.body['description'] == 'role was not granted to user'

    user_cleanup(user)


@pytest.mark.parametrize("sufficient_role,checked_role,user", SUFFICIENT_ROLES_WITH_USER_FOR_GRANT)
async def test_role_check_sufficient_nonex_role(
    sufficient_role,
    checked_role,
    user,
    user_cleanup,
    user_register,
    user_auth_access_header,
    role_assign,
    role_check,
):
    """Проверить несуществующую роль у существующего пользователя"""
    user_cleanup(user)
    response = await user_register(user)
    user_id = response.body['data']['id']
    role_assign(user, sufficient_role)
    user_auth_header = await user_auth_access_header(user)
    data = {'id': user_id, 'name': 'nonexistingrole'}

    response = await role_check(user_auth_header, data)

    assert response.status == 461
    assert response.body['description'] == 'role was not granted to user'

    user_cleanup(user)
