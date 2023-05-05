import uuid

from flask import jsonify, request
from passlib.hash import pbkdf2_sha256
from auth.extensions.jaeger import jaeger_tracing


class ExistingRoles:
    ADMINISTRATOR = 'administrator'
    EDITOR = 'editor'
    SUBSCRIBER = 'subscriber'
    USER = 'user'
    ANONYMOUS = 'anonymous'
    SERVICE = 'service'


class ActivationStatus:
    DIRECT_REGISTRATION_INACTIVE = 0
    DIRECT_REGISTRATION_ACTIVE = 1
    DIRECT_REGISTRATION_BLOCKED = 2

    OAUTH_REGISTRATION_INACTIVE = 10
    OAUTH_REGISTRATION_ACTIVE = 11
    OAUTH_REGISTRATION_BLOCKED = 12


def generate_password(password: str):
    return pbkdf2_sha256\
        .using(rounds=1000, salt_size=10)\
        .hash(password)


def verify_password(password: str, hashed: str):
    return pbkdf2_sha256.verify(password, hashed)


def jsonify_wrapper(
        code: int = 200,
        success: bool = True,
        description: str = '',
        data: str = '{}',
        mimetype: str = 'application/json'
):
    response = jsonify(
        code=code,
        success=success,
        description=description,
        data=data
    )
    response.status_code = code
    response.content_type = mimetype
    return response


@jaeger_tracing()
def handle(
    service_function,
    success_code: int = 200,
    success_description: str = '',
    **kwargs: dict
):
    req = request.get_json(silent=True, force=False, cache=False)
    res = service_function(req, **{**kwargs, **request.args})
    return jsonify_wrapper(
        code=success_code,
        data=res,
        description=success_description
    )


def has_authorization(
    authorized_roles: list,
    user_roles: list,
    superuser=ExistingRoles.ADMINISTRATOR
):
    if superuser in user_roles:
        return True
    return len(set(authorized_roles).intersection(set(user_roles))) > 0


def has_anonymous_in_roles(user):
    for role in user.roles:
        if role.name == ExistingRoles.ANONYMOUS:
            return True
    return False


def make_anonymous_user():
    user_id = str(uuid.uuid4())
    login = user_id.replace('-', '')
    email = "{}@anonymous.local".format(login)
    return {
        'id': user_id,
        'login': login,
        'email': email,
        'name': login,
        'lastname': login,
        'active': ActivationStatus.DIRECT_REGISTRATION_ACTIVE,
        'password': login
    }
