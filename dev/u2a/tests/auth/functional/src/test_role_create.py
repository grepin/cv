from http import HTTPStatus

import pytest

from tests.auth.functional.testdata.role import ROLE, USER

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "user,role,sufficient_role",
    [
        (USER, ROLE, 'administrator'),
        (USER, ROLE, 'editor'),
    ])
async def test_role_create_sufficient(
    user,
    role,
    sufficient_role,
    role_cleanup,
    role_create,
    role_assign,
    user_cleanup,
    user_register,
    user_auth_access_header
):
    """Можно ли создать роль, имея достаточно прав?"""
    user_cleanup(user)
    role_cleanup(role)
    await user_register(user)
    role_assign(user, sufficient_role)
    user_auth_header = await user_auth_access_header(user)

    response = await role_create(user_auth_header, role)

    assert response.status == HTTPStatus.OK
    assert role['name'] in response.body['data']

    role_cleanup(role)
    user_cleanup(user)


@pytest.mark.parametrize(
    "user,role,insufficient_role",
    [
        (USER, ROLE, 'anonymous'),
        (USER, ROLE, 'subscriber'),
    ])
async def test_role_create_insufficient(
    user,
    role,
    insufficient_role,
    role_cleanup,
    role_create,
    role_assign,
    user_cleanup,
    user_register,
    user_auth_access_header
):
    """Можно ли создать роль, не имея достаточно прав?"""
    user_cleanup(user)
    role_cleanup(role)
    await user_register(user)
    role_assign(user, insufficient_role)
    user_auth_header = await user_auth_access_header(user)

    response = await role_create(user_auth_header, role)

    assert response.status == 442
    assert response.body['description'] == 'insufficient rights'

    role_cleanup(role)
    user_cleanup(user)
