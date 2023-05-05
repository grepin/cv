from werkzeug.exceptions import HTTPException


class HTTPExceptionWithData(HTTPException):
    def __init__(
            self,
            code: int = None,
            description: str = None,
            data: dict = None
    ):
        super().__init__()
        if code is not None:
            self.code = code
        if data is not None:
            self.data = data
        if description is not None:
            self.description = description


class HTTPUnauthorized(HTTPExceptionWithData):
    code = 440
    description = 'no access token specified'


class HTTPInvalidCredentials(HTTPExceptionWithData):
    code = 441
    description = 'invalid credentials'


class HTTPInsufficientRights(HTTPExceptionWithData):
    code = 442
    description = 'insufficient rights'


class HTTPNoSuchUser(HTTPExceptionWithData):
    code = 450
    description = 'no such user'


class HTTPConstraintsValidationException(HTTPExceptionWithData):
    code = 451
    description = 'constraints validation error'


class HTTPInputValidationException(HTTPExceptionWithData):
    code = 452
    description = 'input validation error'


class HTTPFieldModificationProhibited(HTTPExceptionWithData):
    code = 453
    description = 'field modification prohibited'


class HTTPExcessiveField(HTTPExceptionWithData):
    code = 454
    description = 'excessive field'


class HTTPMissingField(HTTPExceptionWithData):
    code = 455
    description = 'missing field'


class HTTPAccessTokenRevoked(HTTPExceptionWithData):
    code = 456
    description = 'access token revoked'


class HTTPRefreshTokenNeeded(HTTPExceptionWithData):
    code = 457
    description = 'refresh token needed'


class HTTPRoleNotExists(HTTPExceptionWithData):
    code = 458
    description = 'role not exists'


class HTTPUndeletableRole(HTTPExceptionWithData):
    code = 459
    description = 'undeletable role'


class HTTPRoleHasUsers(HTTPExceptionWithData):
    code = 460
    description = 'role has users, revoke first'


class HTTPNoSuchGrant(HTTPExceptionWithData):
    code = 461
    description = 'role was not granted to user'


class HTTPUnsupportedOAuthProvider(HTTPExceptionWithData):
    code = 462
    description = 'unsupported OAuth2 provider'


class HTTPLoginAgain(HTTPExceptionWithData):
    code = 463
    description = 'need to login again'


class RateLimitExceeded(HTTPExceptionWithData):
    code = 465
    description = 'calm down, rate limit exceeded'


class HTTPTokenExpired(HTTPExceptionWithData):
    code = 466
    description = 'token expired'


class HTTPTokenInvalid(HTTPExceptionWithData):
    code = 467
    description = 'token invalid'
