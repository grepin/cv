from http import HTTPStatus

import pytest

from tests.auth.functional.testdata.user import USER

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("user,http_get", [(USER[0], True), (USER[0], False)])
async def test_update(user, http_get, user_cleanup, user_register, user_auth_access_header, user_sessions):
    """Провека попытки получения свдения о сессии"""
    user_cleanup(user)
    response = await user_register(user)
    assert response.status == HTTPStatus.OK
    auth_headers = await user_auth_access_header(user)

    response = await user_sessions(auth_headers, http_get=http_get)

    assert response.status == HTTPStatus.OK
    assert response.body['description'] == 'sessions retrieved'
    assert response.body['data']['count'] == 1
    assert len(response.body['data']['sessions']) == 1
    assert 'access_token' in response.body['data']['sessions'][0]
    assert 'logon_date' in response.body['data']['sessions'][0]

    user_cleanup(user)
