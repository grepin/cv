from auth.docspecs.response_models import RESPONSE_BASE

E_INTERNAL_ERROR = {**RESPONSE_BASE, **{
  "example": {
    "code": 500,
    "data": {},
    "description": "internal error",
    "success": False
  }
}}


E_NO_SUCH_USER = {**RESPONSE_BASE, **{
  "example": {
    "code": 450,
    "success": False,
    "description": 'no such user',
    "data": {}
  }
}}

E_INVALID_CREDENTIALS = {**RESPONSE_BASE, **{
  "example": {
    "code": 441,
    "data": {},
    "description": "invalid credentials",
    "success": False
  }
}}

E_MISSING_FIELD = {**RESPONSE_BASE, **{
  "example": {
    "code": 455,
    "data": {
      "password": [
        "missing"
      ]
    },
    "description": "missing field",
    "success": False
  }
}}

E_ROLE_CONSTRAINTS_VALIDATION = {**RESPONSE_BASE, **{
  "example": {
    "code": 451,
    "data": {
      "user_id": "not exists"
    },
    "description": "constraints validation error",
    "success": False
  }
}}

E_CONSTRAINTS_VALIDATION = {**RESPONSE_BASE, **{
  "example": {
    "code": 451,
    "data": {
      "login": "already exists"
    },
    "description": "constraints validation error",
    "success": False
  }
}}

E_ROLE_NOT_EXISTS = {**RESPONSE_BASE, **{
  "example": {
    "code": 458,
    "data": {},
    "description": "role not exists",
    "success": False
  }
}}

E_ROLE_UNDELETABLE = {**RESPONSE_BASE, **{
  "example": {
    "code": 459,
    "data": {},
    "description": "undeletable role",
    "success": False
  }
}}


E_INPUT_VALIDATION_ERROR = {**RESPONSE_BASE, **{
  "example": {
    "code": 452,
    "data": {
      "login": [
        "Missing data for required field."
      ],
      "password": [
        "Missing data for required field."
      ]
    },
    "description": "input validation error",
    "success": False
  }
}}


E_NO_ACCESS_TOKEN_SPECIFIED = {**RESPONSE_BASE, **{
  "example": {
    "code": 440,
    "data": "{}",
    "description": "no access token specified",
    "success": False
  }
}}

E_REFRESH_TOKEN_NEEDED = {**RESPONSE_BASE, **{
  "example": {
    "code": 457,
    "data": {},
    "description": "refresh token needed",
    "success": False
  }
}}

E_UNSUPPORTED_OAUTH_PROVIDER = {**RESPONSE_BASE, **{
  "example": {
    "code": 462,
    "data": {},
    "description": "unsupported OAuth2 provider",
    "success": False
  }
}}

E_TOKEN_INVALID = {**RESPONSE_BASE, **{
  "example": {
    "code": 467,
    "data": "Not enough segments",
    "description": "token invalid",
    "success": False
  }
}}

E_RATE_LIMIT_EXCEEDED = {**RESPONSE_BASE, **{
  "example": {
    "code": 465,
    "data": {},
    "description": "calm down, rate limit exceeded",
    "success": False
  }
}}

E_TOKEN_EXPIRED = {**RESPONSE_BASE, **{
  "example": {
      "code": 466,
      "data": {
        "active": False,
        "email": "adam@mankind.com",
        "exp": 1652646104,
        "fresh": 1652646104.071702,
        "iat": 1652646074,
        "id": "6c3cd8a0-8d75-45e0-beb6-930ee513c686",
        "jti": "7c51331c-4f4d-410b-8833-27a3937907d0",
        "lastname": "firstman",
        "login": "adam",
        "name": "adam",
        "nbf": 1652646074,
        "roles": {
          "user": "823ce223-4923-42a9-b70e-2f517638e9de"
        },
        "sub": "6c3cd8a0-8d75-45e0-beb6-930ee513c686",
        "type": "access"
      },
      "description": "token expired",
      "success": False
    }
  }
}


E_INSUFFICIENT_RIGHTS = {**RESPONSE_BASE, **{
  "example": {
    "code": 442,
    "data": {},
    "description": "insufficient rights",
    "success": False
  }
}}

E_ACCESS_TOKEN_REVOKED = {**RESPONSE_BASE, **{
  "example": {
    "code": 456,
    "data": {
      "active": 1,
      "email": "adam@mankind.com",
      "exp": 1654875375,
      "fresh": 1654875105.177956,
      "iat": 1654875075,
      "id": "64a13e87-5a5d-403c-b886-2a785c9eb7b0",
      "jti": "44fabeca-b2ef-4b94-9906-0b1896ad5ae5",
      "lastname": "null",
      "login": "adam",
      "name": "null",
      "nbf": 1654875075,
      "roles": {
        "administrator": "0a7c7482-ff98-4a4a-b4dc-a7c6075c8c17",
        "subscriber": "9744d299-abc6-48a9-8862-0357cd4355a9",
        "user": "bf63a7a4-3847-4cc7-8a01-7d7db34f9301"
      },
      "sub": "64a13e87-5a5d-403c-b886-2a785c9eb7b0",
      "type": "access"
    },
    "description": "access token revoked",
    "success": False
  }
}}

E_ROLE_NOT_GRANTED = {**RESPONSE_BASE, **{
  "example": {
    "code": 461,
    "data": {},
    "description": "role was not granted to user",
    "success": False
  }
}}

E_NOT_UUID = {**RESPONSE_BASE, **{
  "example": {
    "code": 452,
    "data": {
      "role_id": [
        "Not a valid UUID."
      ]
    },
    "description": "input validation error",
    "success": False
  }
}}




# class HTTPUnauthorized(HTTPExceptionWithData):
#     code = 401
#     description = 'no access token specified'
#
#
# class HTTPInsufficientRights(HTTPExceptionWithData):
#     code = 402
#     description = 'insufficient rights'
#
#
#
#
# class HTTPInputValidationException(HTTPExceptionWithData):
#     code = 452
#     description = 'input validation error'
#
#
# class HTTPFieldModificationProhibited(HTTPExceptionWithData):
#     code = 453
#     description = 'field modification prohibited'
#
#
# class HTTPExcessiveField(HTTPExceptionWithData):
#     code = 454
#     description = 'excessive field'
#
#
# class HTTPMissingField(HTTPExceptionWithData):
#     code = 455
#     description = 'missing field'
#
#
# class HTTPAccessTokenRevoked(HTTPExceptionWithData):
#     code = 456
#     description = 'access token revoked'
#
#
# class HTTPRefreshTokenNeeded(HTTPExceptionWithData):
#     code = 457
#     description = 'refresh token needed'
#
#
# class HTTPRoleNotExists(HTTPExceptionWithData):
#     code = 458
#     description = 'role not exists'
#
#
# class HTTPUndeletableRole(HTTPExceptionWithData):
#     code = 459
#     description = 'undeletable role'
#
#
# class HTTPRoleHasUsers(HTTPExceptionWithData):
#     code = 460
#     description = 'role has users, revoke first'
#
#
# class HTTPNoSuchGrant(HTTPExceptionWithData):
#     code = 461
#     description = 'role was not granted to user'
