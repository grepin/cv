from http import HTTPStatus

import pytest

from tests.auth.functional.settings import JWT_SECRET_KEY
from tests.auth.functional.testdata.user import USER
from tests.auth.functional.utils import get_auth_header, get_token_data

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("user,http_get", [(USER[0], True), (USER[0], False)])
async def test_terminate(user, http_get, user_cleanup, user_register, user_auth_tokens, user_terminate, user_refresh):
    """Раотает ли полное прерывание всех сессий пользоваля, включая инвалидацию refresh?"""

    user_cleanup(user)
    await user_register(user)
    access1, refresh1 = await user_auth_tokens(user)
    access2, refresh2 = await user_auth_tokens(user)

    response = await user_terminate(get_auth_header(access1), http_get=http_get)
    response_access1 = await user_terminate(get_auth_header(access1), http_get=http_get)
    response_access2 = await user_terminate(get_auth_header(access2), http_get=http_get)
    response_refresh1 = await user_refresh(get_auth_header(refresh1), http_get=http_get)
    response_refresh2 = await user_refresh(get_auth_header(refresh2), http_get=http_get)

    assert response.status == HTTPStatus.OK
    assert response.body['data'] == {}
    assert response.body['description'] == 'all sessions terminated'
    assert response_access1.status == 456
    assert response_access1.body['data'] == get_token_data(access1, JWT_SECRET_KEY)
    assert response_access2.status == 456
    assert response_access2.body['data'] == get_token_data(access2, JWT_SECRET_KEY)
    assert response_refresh1.status == 456
    assert response_refresh1.body['data'] == get_token_data(refresh1, JWT_SECRET_KEY)
    assert response_refresh2.status == 456
    assert response_refresh2.body['data'] == get_token_data(refresh2, JWT_SECRET_KEY)

    user_cleanup(user)
