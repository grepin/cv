import re
from functools import wraps

from flask_jwt_extended.exceptions import WrongTokenError
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

from auth.utils.functional import has_authorization
from auth.utils.http_exceptions import (HTTPConstraintsValidationException,
                                        HTTPInputValidationException,
                                        HTTPInsufficientRights,
                                        HTTPRefreshTokenNeeded)


def wrap_errors_in_http(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IntegrityError as e:
            data = {}
            g = re.search(r'DETAIL:.*\(([a-zA-Z0-9 ,_]+)\)=.*already exists', e._message())
            if g is not None:
                data = {g.group(1): 'already exists'}
            else:
                g = re.search(r'DETAIL:.*\(([a-zA-Z0-9 ,_]+)\)=.*is not present in table', e._message())
                if g is not None:
                    data = {g.group(1): 'not exists'}
            raise HTTPConstraintsValidationException(data=data)
        except ValidationError as e:
            raise HTTPInputValidationException(data=e.messages)
        except WrongTokenError:
            raise HTTPRefreshTokenNeeded(data={})
    return inner


def jwt_authorization_required(
    authorized_roles: list,
    user_data_func
):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            user_roles = user_data_func()['roles'].keys()
            if has_authorization(authorized_roles, user_roles) is False:
                raise HTTPInsufficientRights()
            return func(*args, **kwargs)
        return inner
    return wrapper
