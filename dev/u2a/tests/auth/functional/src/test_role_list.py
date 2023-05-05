from http import HTTPStatus

import pytest

from tests.auth.functional.testdata.role import \
    SUFFICIENT_ROLES_WITH_USER_FOR_LIST

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("sufficient_role,user", SUFFICIENT_ROLES_WITH_USER_FOR_LIST)
async def test_role_create_sufficient(
    sufficient_role,
    user,
    user_cleanup,
    user_register,
    user_auth_access_header,
    role_assign,
    role_list
):
    """Получить все роли и убедиться, что по меньшей мере все hardcoded присутствуют"""
    user_cleanup(user)
    await user_register(user)
    role_assign(user, sufficient_role)
    user_auth_header = await user_auth_access_header(user)

    response = await role_list(user_auth_header)

    assert response.status == HTTPStatus.OK
    assert 'administrator' in response.body['data']

    user_cleanup(user)
