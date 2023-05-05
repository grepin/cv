import asyncio
import random
import string
from dataclasses import dataclass

import aiohttp
import pytest
import redis
from multidict import CIMultiDictProxy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

from tests.auth.functional.settings import (AUTH_API_HOST, AUTH_API_PATH_V1,
                                            REDIS_ACCESS_TOKENS_DB, REDIS_HOST,
                                            REDIS_PASSWORD, REDIS_PORT,
                                            REDIS_REFRESH_TOKENS_DB,
                                            SQLALCHEMY_DATABASE_URI, JWT_SECRET_KEY)
from tests.auth.functional.utils import get_auth_header, get_token_data


@pytest.fixture(scope='session')
def db():
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    db_session = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )
    )
    yield db_session
    db_session.close()


class DBFields:
    login = 'login'
    email = 'email'
    id = 'id'
    user_id = 'user_id'
    role_id = 'role_id'
    name = 'name'


class DBTables:
    users = 'users'
    roles = 'roles'
    user2role = 'user2role'
    sessions = 'sessions'


@pytest.fixture
def dbe():
    class DBEntities:
        table = DBTables()
        field = DBFields()

    return DBEntities()


@pytest.fixture
def user_cleanup(db, dbe):
    def inner(user):
        s = "SELECT {} FROM {} WHERE ".format(dbe.field.id, dbe.table.users)
        d = {}
        if dbe.field.login in user:
            s += dbe.field.login + ' = :' + dbe.field.login
            d[dbe.field.login] = user[dbe.field.login]
        if dbe.field.email in user:
            if dbe.field.login in user:
                s += ' OR '
            s += dbe.field.email + ' = :' + dbe.field.email
            d[dbe.field.email] = user[dbe.field.email]
        user_ids = db.execute(text(s), d).all()
        db.commit()
        if user_ids is not None:
            for user_id_entry in user_ids:
                user_id = user_id_entry[0]

                s2 = "DELETE FROM {} WHERE {} = :{}".format(dbe.table.user2role, dbe.field.user_id, dbe.field.user_id)
                d2 = {dbe.field.user_id: user_id}
                db.execute(text(s2), d2)
                db.commit()

                s = "DELETE FROM {} WHERE {} = :{}".format(dbe.table.users, dbe.field.id, dbe.field.id)
                d = {dbe.field.id: user_id}
                db.execute(text(s), d)
                db.commit()
    return inner


@pytest.fixture
def role_assign(db, dbe):
    def inner(user, role):

        s = "SELECT {} FROM {} WHERE ".format(dbe.field.id, dbe.table.users)
        d = {}
        if dbe.field.login in user:
            s += dbe.field.login + ' = :' + dbe.field.login
            d[dbe.field.login] = user[dbe.field.login]
        if dbe.field.email in user:
            if dbe.field.login in user:
                s += ' OR '
            s += dbe.field.email + ' = :' + dbe.field.email
            d[dbe.field.email] = user[dbe.field.email]
        user_ids = db.execute(text(s), d).first()
        db.commit()
        if user_ids is not None:
            user_id = user_ids[0]
            s2 = "INSERT INTO {} ({}, {}) SELECT '{}', {}.{} FROM {} WHERE {}.{} = :{}".format(
                dbe.table.user2role,
                dbe.field.user_id,
                dbe.field.role_id,
                user_id,
                dbe.table.roles, dbe.field.id,
                dbe.table.roles,
                dbe.table.roles, dbe.field.name,
                dbe.field.name
            )
            d = {dbe.field.name: role}
            db.execute(text(s2), d)
            db.commit()

    return inner


@pytest.fixture
def get_role_id(db, dbe):
    def inner(role_name):

        s = "SELECT {} FROM {} WHERE {} = :{}".format(
            dbe.field.id,
            dbe.table.roles,
            dbe.field.name,
            dbe.field.name,
        )
        d = {dbe.field.name: role_name}
        return str(db.execute(text(s), d).first()[0])
    return inner


@pytest.fixture(autouse=True)
def sessions_cleanup(db, dbe):
    s = "DELETE FROM {}".format(dbe.table.sessions)
    db.execute(text(s))
    db.commit()


@pytest.fixture
def role_cleanup(db, dbe):
    def inner(role):
        s = "SELECT {} FROM {} WHERE {} = :{}".format(dbe.field.id, dbe.table.roles, dbe.field.name, dbe.field.name)
        role_ids = db.execute(text(s), {dbe.field.name: role[dbe.field.name]}).first()
        db.commit()
        if role_ids is not None:
            role_id = role_ids[0]

            s2 = "DELETE FROM {} WHERE {} = :{}".format(dbe.table.user2role, dbe.field.role_id, dbe.field.role_id)
            d2 = {dbe.field.role_id: role_id}
            db.execute(text(s2), d2)
            db.commit()

            s = "DELETE FROM {} WHERE {} = :{}".format(dbe.table.roles, dbe.field.id, dbe.field.id)
            d = {dbe.field.id: role_id}
            db.execute(text(s), d)
            db.commit()

    return inner


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()


@pytest.fixture(scope='session')
async def session():
    connector = aiohttp.TCPConnector(limit=100, force_close=True, enable_cleanup_closed=True)
    session = aiohttp.ClientSession(connector=connector)
    yield session
    await session.close()


@pytest.fixture
def post_request(session):
    async def inner(
            path: str,
            method: str,
            headers: dict = {},
            json: dict = {}
    ) -> HTTPResponse:
        uri = path + method
        async with session.post(uri, headers=headers, json=json) as response:
            body = await response.json()
            return HTTPResponse(
                body=body,
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
def delete_request(session):
    async def inner(
            path: str,
            method: str,
            headers: dict = {},
            json: dict = {}
    ) -> HTTPResponse:
        uri = path + method
        async with session.delete(uri, headers=headers, json=json) as response:
            body = await response.json()
            return HTTPResponse(
                body=body,
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
def put_request(session):
    async def inner(
            path: str,
            method: str,
            headers: dict = {},
            json: dict = {}
    ) -> HTTPResponse:
        uri = path + method
        async with session.put(uri, headers=headers, json=json) as response:
            body = await response.json()
            return HTTPResponse(
                body=body,
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
def get_request(session):
    async def inner(
            path: str,
            method: str,
            headers: dict = {},
            params: dict = {}
    ) -> HTTPResponse:
        uri = path + method
        async with session.get(uri, headers=headers, params=params) as response:
            body = await response.json()
            return HTTPResponse(
                body=body,
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
def auth_v1_path():
    return AUTH_API_HOST + AUTH_API_PATH_V1


@pytest.fixture
def user_register(auth_v1_path, post_request):
    async def inner(user):
        return await post_request(
            path=auth_v1_path,
            method="/user/register",
            json=user
        )

    return inner


@pytest.fixture
def role_create(auth_v1_path, post_request):
    async def inner(header, role):
        return await post_request(
            path=auth_v1_path,
            method="/role/create",
            headers=header,
            json=role
        )

    return inner


@pytest.fixture
def role_grant(auth_v1_path, post_request):
    async def inner(header, data):
        return await post_request(
            path=auth_v1_path,
            method="/role/grant",
            headers=header,
            json=data
        )

    return inner


@pytest.fixture
def role_revoke(auth_v1_path, post_request):
    async def inner(header, data):
        return await post_request(
            path=auth_v1_path,
            method="/role/revoke",
            headers=header,
            json=data
        )
    return inner


@pytest.fixture
def role_check(auth_v1_path, post_request):
    async def inner(header, data):
        return await post_request(
            path=auth_v1_path,
            method="/role/check",
            headers=header,
            json=data
        )
    return inner


@pytest.fixture
def role_list(auth_v1_path, get_request):
    async def inner(header):
        return await get_request(
            path=auth_v1_path,
            method="/role/list",
            headers=header,
        )

    return inner


@pytest.fixture
def user_login(auth_v1_path, post_request):
    async def inner(user, cleanup=True):
        if cleanup:
            u = {
                'login': user['login'],
                'password': user['password']
            }
        else:
            u = user
        return await post_request(
            path=auth_v1_path,
            method="/user/login",
            json=u,
        )

    return inner


@pytest.fixture
def welcome(auth_v1_path, post_request):
    async def inner():
        return await post_request(
            path=auth_v1_path,
            method="/user/welcome",
        )
    return inner


@pytest.fixture
def welcome_auth_tokens(auth_v1_path, welcome):
    async def inner():
        response = await welcome()
        access = response.body['data']['access_token']
        refresh = response.body['data']['refresh_token']
        return access, refresh
    return inner


@pytest.fixture
def welcome_auth_access_header_and_data(auth_v1_path, post_request, welcome):
    async def inner(use_refresh=False):
        response = await welcome()
        token = response.body['data']['refresh_token'] if use_refresh else response.body['data']['access_token']
        return get_auth_header(token), get_token_data(token, JWT_SECRET_KEY)
    return inner


@pytest.fixture
def user_logout(auth_v1_path, post_request, get_request):
    async def inner(auth_headers: dict, http_get=True):
        hm = get_request if http_get else post_request
        return await hm(
            path=auth_v1_path,
            method="/user/logout",
            headers=auth_headers
        )

    return inner


@pytest.fixture
def user_terminate(auth_v1_path, post_request, get_request):
    async def inner(auth_headers: dict, http_get=True):
        hm = get_request if http_get else post_request
        return await hm(
            path=auth_v1_path,
            method="/user/terminate",
            headers=auth_headers
        )

    return inner


@pytest.fixture
def user_sessions(auth_v1_path, post_request, get_request):
    async def inner(auth_headers: dict, http_get=True):
        hm = get_request if http_get else post_request
        return await hm(
            path=auth_v1_path,
            method="/user/sessions",
            headers=auth_headers
        )

    return inner


@pytest.fixture
def user_refresh(auth_v1_path, post_request, get_request):
    async def inner(auth_headers: dict, http_get=True):
        hm = get_request if http_get else post_request
        return await hm(
            path=auth_v1_path,
            method="/user/refresh",
            headers=auth_headers
        )

    return inner


@pytest.fixture
def user_auth_tokens(auth_v1_path, post_request, user_login):
    async def inner(user, cleanup=True):
        response = await user_login(user, cleanup)
        access = response.body['data']['access_token']
        refresh = response.body['data']['refresh_token']
        return access, refresh

    return inner


@pytest.fixture
def user_auth_access_header(auth_v1_path, post_request, user_login):
    async def inner(user, cleanup=True, use_refresh=False):
        response = await user_login(user, cleanup)
        token = response.body['data']['refresh_token'] if use_refresh else response.body['data']['access_token']
        return get_auth_header(token)

    return inner


@pytest.fixture
def user_update(auth_v1_path, put_request):
    async def inner(auth_headers, updated_user):
        return await put_request(
            path=auth_v1_path,
            method="/user/update",
            headers=auth_headers,
            json=updated_user
        )

    return inner


@pytest.fixture
def role_delete(auth_v1_path, delete_request):
    async def inner(auth_headers, role):
        return await delete_request(
            path=auth_v1_path,
            method="/role/delete",
            headers=auth_headers,
            json=role
        )

    return inner


@pytest.fixture
def random_string():
    def inner(length: int):
        return ''.join(
            random.choice(
                string.ascii_uppercase + string.digits
            ) for _ in range(length)
        )

    return inner


@pytest.fixture(scope='session')
def redis4access():
    client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        db=REDIS_ACCESS_TOKENS_DB)
    yield client
    client.close()


@pytest.fixture(scope='session')
def redis4refresh():
    client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        db=REDIS_REFRESH_TOKENS_DB)
    yield client
    client.close()


@pytest.fixture
def redis_get(redis4access, redis4refresh):
    async def inner(key: str, access=True) -> None:
        r = redis4access if access else redis4refresh
        redis_cache_data = r.get(key)
        if redis_cache_data:
            return redis_cache_data.decode()
        return None

    return inner


@pytest.fixture
def redis_delete(redis4access, redis4refresh):
    async def inner(key: str, access=True) -> None:
        r = redis4access if access else redis4refresh
        return r.delete(key)

    return inner


@pytest.fixture
def redis_set(redis4access, redis4refresh):
    async def inner(key: str, value: str, access=True, ex=10) -> None:
        r = redis4access if access else redis4refresh
        return r.setex(key, ex, value)

    return inner
