from http import HTTPStatus

import pytest

from tests.auth.functional.testdata.role import \
    SUFFICIENT_ROLES_WITH_USER_FOR_GRANT

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("sufficient_role,revoked_role,user", SUFFICIENT_ROLES_WITH_USER_FOR_GRANT)
async def test_role_revoke_sufficient(
    sufficient_role,
    revoked_role,
    user,
    user_cleanup,
    user_register,
    user_auth_access_header,
    role_assign,
    role_revoke,
    get_role_id
):
    """Отозвать у пользователя одну из присвоенных ролей"""
    user_cleanup(user)
    response = await user_register(user)
    user_id = response.body['data']['id']
    role_assign(user, sufficient_role)
    role_assign(user, revoked_role)
    role_id = get_role_id(revoked_role)
    user_auth_header = await user_auth_access_header(user)
    data = {'user_id': user_id, 'role_id': role_id}

    response = await role_revoke(user_auth_header, data)

    assert response.status == HTTPStatus.OK
    assert response.body['data']['user_id'] == user_id
    assert response.body['data']['role_id'] == role_id

    user_cleanup(user)


@pytest.mark.parametrize("sufficient_role,revoked_role,user", SUFFICIENT_ROLES_WITH_USER_FOR_GRANT)
async def test_role_revoke_sufficient_notgranted(
    sufficient_role,
    revoked_role,
    user,
    user_cleanup,
    user_register,
    user_auth_access_header,
    role_assign,
    role_revoke,
    get_role_id
):
    """Отозвать у пользователя не присвоенную ему роль"""
    user_cleanup(user)
    response = await user_register(user)
    user_id = response.body['data']['id']
    role_assign(user, sufficient_role)
    role_id = get_role_id(revoked_role)
    user_auth_header = await user_auth_access_header(user)
    data = {'user_id': user_id, 'role_id': role_id}

    response = await role_revoke(user_auth_header, data)

    assert response.status == 461
    assert response.body['description'] == 'role was not granted to user'

    user_cleanup(user)
