from datetime import timedelta

from flask_jwt_extended import (JWTManager, create_access_token,
                                create_refresh_token, decode_token,
                                get_current_user, get_jwt)

from auth.core.config import (JWT_ACCESS_TOKEN_EXPIRES_SECONDS,
                              JWT_REFRESH_TOKEN_EXPIRES_SECONDS,
                              JWT_SECRET_KEY)
from auth.extensions.flask import app
from auth.models.models import Role
from auth.models.schemas import UserSchema, UserSchema4JWT
from auth.utils.functional import jsonify_wrapper, ExistingRoles
from auth.utils.http_exceptions import (
    HTTPAccessTokenRevoked,
    HTTPUnauthorized,
    HTTPTokenExpired,
    HTTPTokenInvalid
)

jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = \
    timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRES_SECONDS)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = \
    timedelta(seconds=JWT_REFRESH_TOKEN_EXPIRES_SECONDS)


@jwt.user_identity_loader
def user_identity_lookup(user_id):
    return user_id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    user = UserSchema4JWT().load(jwt_data.copy(), partial=True)
    user.roles = [Role(id=id, name=name) for name, id in jwt_data['roles'].items()]
    return user


@jwt.unauthorized_loader
def unauthorized(e):
    ue = HTTPUnauthorized()
    return jsonify_wrapper(code=ue.code, description=ue.description)


def gen_token(
    identity,
    expires,
    access: bool = True,
    fresh: int = 0,
    additional_claims={},
):
    if access is True:
        return create_access_token(
            identity=identity,
            fresh=False if fresh == 0 else timedelta(seconds=fresh),
            additional_claims=additional_claims,
            expires_delta=timedelta(seconds=expires)
        )
    return create_refresh_token(
        identity=identity,
        additional_claims=additional_claims,
        expires_delta=timedelta(seconds=expires)
    )


def _token_redis_key(user_id: str, jti: str):
    return "{}:{}".format(user_id, jti)


def _token_data(data: dict):
    user_id = data['id']
    access = data['type'] == 'access'
    expires = data['exp']
    jti = data['jti']
    return user_id, access, expires, jti, _token_redis_key(user_id, jti)


def _parse_token(token: str):
    data = decode_token(token)
    return _token_data(data)


def is_token_data_valid(data: dict):
    user_id, access, expires, jti, key = _token_data(data)
    if access:
        return app.redis4access.get(key) is None
    else:
        return app.redis4refresh.get(key) is not None


def is_token_valid(token: str):
    return is_token_data_valid(_parse_token(token))


def invalidate_token_by_key(
        key: str,
        expires: int = JWT_ACCESS_TOKEN_EXPIRES_SECONDS,
        access: bool = True):
    if access:
        return app.redis4access.setex(key, expires, 0)
    else:
        return app.redis4refresh.delete(key)


def current_user():
    return get_current_user()


def current_user_as_dict():
    return UserSchema().dump(get_current_user())


def invalidate_current_token():
    user_id, access, expires, jti, key = _token_data(get_jwt())
    invalidate_token_by_key(key, expires, access=access)


def invalidate_token(token: str):
    user_id, access, expires, jti, key = _parse_token(token)
    invalidate_token_by_key(key, expires, access=access)


def revalidate_refresh_token(actual: str, invalid: str = None):
    if invalid is not None:
        invalidate_token(invalid)
    user_id, access, expires, jti, key = _parse_token(actual)
    app.redis4refresh.setex(key, expires, 0)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    if ExistingRoles.ANONYMOUS in jwt_payload['roles']:
        return False
    return not is_token_data_valid(jwt_payload)


@jwt.revoked_token_loader
def token_revoked(jwt_header, jwt_payload: dict):
    te = HTTPAccessTokenRevoked()
    return jsonify_wrapper(
        code=te.code,
        data=jwt_payload,
        description=te.description,
        success=False)


@jwt.expired_token_loader
def token_expired(jwt_header, jwt_payload):
    te = HTTPTokenExpired()
    return jsonify_wrapper(
        code=te.code,
        data=jwt_payload,
        description=te.description,
        success=False)


@jwt.invalid_token_loader
def token_invalid(jwt_payload):
    te = HTTPTokenInvalid()
    return jsonify_wrapper(
        code=te.code,
        data=jwt_payload,
        description=te.description,
        success=False)
