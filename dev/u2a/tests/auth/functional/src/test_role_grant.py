from http import HTTPStatus

import pytest

from tests.auth.functional.testdata.role import \
    SUFFICIENT_ROLES_WITH_USER_FOR_GRANT

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("sufficient_role,granted_role,user", SUFFICIENT_ROLES_WITH_USER_FOR_GRANT)
async def test_role_grant_sufficient(
    sufficient_role,
    granted_role,
    user,
    user_cleanup,
    user_register,
    user_auth_access_header,
    role_assign,
    role_grant,
    get_role_id
):
    """Присвоить пользователю одну из существующих ролей"""
    user_cleanup(user)
    response = await user_register(user)
    user_id = response.body['data']['id']
    role_assign(user, sufficient_role)
    role_id = get_role_id(granted_role)
    user_auth_header = await user_auth_access_header(user)
    data = {'user_id': user_id, 'role_id': role_id}

    response = await role_grant(user_auth_header, data)

    assert response.status == HTTPStatus.OK
    assert response.body['data']['user_id'] == user_id
    assert response.body['data']['role_id'] == role_id

    user_cleanup(user)


@pytest.mark.parametrize("sufficient_role,granted_role,user", SUFFICIENT_ROLES_WITH_USER_FOR_GRANT)
async def test_role_grant_sufficient_twice(
    sufficient_role,
    granted_role,
    user,
    user_cleanup,
    user_register,
    user_auth_access_header,
    role_assign,
    role_grant,
    get_role_id
):
    """Присвоить пользователю одну из существующих ролей повторно"""
    user_cleanup(user)
    response = await user_register(user)
    user_id = response.body['data']['id']
    role_assign(user, sufficient_role)
    role_id = get_role_id(granted_role)
    user_auth_header = await user_auth_access_header(user)
    data = {'user_id': user_id, 'role_id': role_id}
    await role_grant(user_auth_header, data)  # grant подразумевает terminate all sessions
    user_auth_header = await user_auth_access_header(user)

    response = await role_grant(user_auth_header, data)

    assert response.status == 451
    assert response.body['data']['user_id, role_id'] == 'already exists'

    user_cleanup(user)


@pytest.mark.parametrize("sufficient_role,granted_role,user", SUFFICIENT_ROLES_WITH_USER_FOR_GRANT)
async def test_role_grant_sufficient_nonex_role(
    sufficient_role,
    granted_role,
    user,
    user_cleanup,
    user_register,
    user_auth_access_header,
    role_assign,
    role_grant
):
    """Присвоить пользователю несуществующую роль"""
    user_cleanup(user)
    response = await user_register(user)
    user_id = response.body['data']['id']
    role_assign(user, sufficient_role)
    role_id = '123e4567-0000-0000-0000-426614174000'
    user_auth_header = await user_auth_access_header(user)
    data = {'user_id': user_id, 'role_id': role_id}

    response = await role_grant(user_auth_header, data)

    assert response.status == 451
    assert response.body['data']['role_id'] == 'not exists'

    user_cleanup(user)


@pytest.mark.parametrize("sufficient_role,granted_role,user", SUFFICIENT_ROLES_WITH_USER_FOR_GRANT)
async def test_role_grant_sufficient_ex_role_to_nonex(
    sufficient_role,
    granted_role,
    user,
    user_cleanup,
    user_register,
    user_auth_access_header,
    role_assign,
    role_grant,
    get_role_id
):
    """Присвоить несуществующему пользователю одну из существующих ролей"""
    user_cleanup(user)
    response = await user_register(user)
    user_id = '123e4567-0000-0000-0000-426614174000'
    role_assign(user, sufficient_role)
    role_id = get_role_id(granted_role)
    user_auth_header = await user_auth_access_header(user)
    data = {'user_id': user_id, 'role_id': role_id}

    response = await role_grant(user_auth_header, data)

    assert response.status == 451
    assert response.body['data']['user_id'] == 'not exists'

    user_cleanup(user)
