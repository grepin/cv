import pytest

from tests.auth.functional.testdata.role import ROLE, USER

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "user,role,sufficient_role",
    [
        (USER, ROLE, 'administrator'),
        (USER, ROLE, 'editor'),
    ])
async def test_role_with_users_delete_sufficient(
    user,
    role,
    sufficient_role,
    role_cleanup,
    role_delete,
    role_create,
    role_assign,
    user_cleanup,
    user_register,
    user_auth_access_header
):
    """Можно ли удалить роль, у которой есть пользователи,
        даже имея достаточно прав?
    """
    user_cleanup(user)
    role_cleanup(role)
    await user_register(user)
    role_assign(user, sufficient_role)
    user_auth_header = await user_auth_access_header(user)
    await role_create(user_auth_header, role)
    role_assign(user, role['name'])
    req2delete = {'name': role['name']}

    response = await role_delete(user_auth_header, req2delete)

    assert response.status == 460
    assert response.body['description'] == 'role has users, revoke first'

    role_cleanup(role)
    user_cleanup(user)


@pytest.mark.parametrize(
    "user,role,sufficient_role",
    [
        (USER, ROLE, 'administrator'),
        (USER, ROLE, 'editor'),
    ])
async def test_role_with_no_users_delete_sufficient(
    user,
    role,
    sufficient_role,
    role_cleanup,
    role_delete,
    role_create,
    role_assign,
    user_cleanup,
    user_register,
    user_auth_access_header
):
    """Можно ли удалить роль, у которой нет пользователей,
        даже имея достаточно прав?
    """
    user_cleanup(user)
    role_cleanup(role)
    await user_register(user)
    role_assign(user, sufficient_role)
    user_auth_header = await user_auth_access_header(user)
    await role_create(user_auth_header, role)
    req2delete = {'name': role['name']}

    response = await role_delete(user_auth_header, req2delete)

    assert response.status == 200
    assert role['name'] in response.body['data']

    role_cleanup(role)
    user_cleanup(user)


@pytest.mark.parametrize(
    "user,role,insufficient_role",
    [
        (USER, ROLE, 'subscriber'),
        (USER, ROLE, 'anonymous'),
    ])
async def test_role_delete_insufficient(
    user,
    role,
    insufficient_role,
    role_cleanup,
    role_delete,
    role_create,
    role_assign,
    user_cleanup,
    user_register,
    user_auth_access_header
):
    """Можно ли удалить роль, не имея достаточно прав?"""
    user_cleanup(user)
    role_cleanup(role)
    await user_register(user)
    role_assign(user, insufficient_role)
    user_auth_header = await user_auth_access_header(user)
    await role_create(user_auth_header, role)
    req2delete = {'name': role['name']}

    response = await role_delete(user_auth_header, req2delete)

    assert response.status == 442
    assert response.body['description'] == 'insufficient rights'

    role_cleanup(role)
    user_cleanup(user)


@pytest.mark.parametrize(
    "user,role_to_delete,sufficient_role",
    [
        (USER, {'name': 'editor'}, 'administrator', ),
        (USER, {'name': 'administrator'}, 'editor', ),
    ])
async def test_role_delete_sufficient_undeletable(
    user,
    role_to_delete,
    sufficient_role,
    role_assign,
    role_delete,
    user_cleanup,
    user_register,
    user_auth_access_header
):
    """Можно ли удалить роль, имея достаточно прав?"""
    user_cleanup(user)
    await user_register(user)
    role_assign(user, sufficient_role)
    user_auth_header = await user_auth_access_header(user)

    response = await role_delete(user_auth_header, role_to_delete)

    assert response.status == 459
    assert response.body['description'] == 'undeletable role'

    user_cleanup(user)
