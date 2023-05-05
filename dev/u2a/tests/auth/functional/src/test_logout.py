from http import HTTPStatus

import pytest

from tests.auth.functional.testdata.user import USER

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("user,http_get", [(USER[0], True), (USER[0], False)])
async def test_logout(user, http_get, user_cleanup, user_register, user_auth_access_header, user_logout, redis_get):
    """Работает ли вызов logout для залогиненного пользователя?"""

    user_cleanup(user)
    response = await user_register(user)
    assert response.status == HTTPStatus.OK
    header = await user_auth_access_header(user)

    response = await user_logout(header, http_get=http_get)

    assert response.status == HTTPStatus.OK
    assert response.body['description'] == 'logged out successfully'

    user_cleanup(user)
