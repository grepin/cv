from auth.docspecs.http_exceptions import (
  E_ROLE_CONSTRAINTS_VALIDATION,
  E_INTERNAL_ERROR,
  E_RATE_LIMIT_EXCEEDED,
  E_NO_ACCESS_TOKEN_SPECIFIED,
  E_TOKEN_INVALID,
  E_TOKEN_EXPIRED,
  E_INSUFFICIENT_RIGHTS,
  E_ACCESS_TOKEN_REVOKED,
  E_ROLE_NOT_GRANTED,
  E_NOT_UUID
)
from auth.docspecs.request_models import USER2ROLE
from auth.docspecs.response_models import RESPONSE_BASE

R_ROLE_REVOKE_SUCCESS = {**RESPONSE_BASE, **{
  "example": {
    "code": 200,
    "data": {
      "id": "15f4d519-3eae-4251-abde-ec12f1ef454d",
      "role_id": "9744d299-abc6-48a9-8862-0357cd4355a9",
      "user_id": "64a13e87-5a5d-403c-b886-2a785c9eb7b0"
    },
    "description": "role revoked",
    "success": True
  }
}}


ROLE_REVOKE = {
  "tags": [
    "Удаление роли у существующего пользователя"
  ],
  "security": [{"Bearer": []}],
  "description": """
  Удаляет роль у существующего пользователя, имеющего эту роль. После удаления все токены пользоватля инвалидируются.
  Для получения данных, пользователь (идентифицируемый токеном) должен иметь роль administrator или editor
  """,
  "parameters": [
    {
      "in": "body",
      "name": "payload",
      "schema": USER2ROLE
    },
  ],
  "responses": {
    "200": {
      "description": "Успешно, выбранная роль присвоена выбранному пользователю",
      "schema": R_ROLE_REVOKE_SUCCESS
    },
    "465": {
      "description": "Если превышено допустимое число запросов в единицу времени",
      "schema": E_RATE_LIMIT_EXCEEDED
    },
    "440": {
      "description": "Если не указан acces-токен в заголовке авторизации",
      "schema": E_NO_ACCESS_TOKEN_SPECIFIED
    },
    "442": {
      "description": "У пользователя недостаточно прав",
      "schema": E_INSUFFICIENT_RIGHTS
    },
    "452": {
      "description": "Если user_id или role_id не соответствуют формату UUID",
      "schema": E_NOT_UUID
    },
    "456": {
      "description": "Если токен был отозван",
      "schema": E_ACCESS_TOKEN_REVOKED
    },
    "461": {
      "description": "Если роль не была присвоена пользователю",
      "schema": E_ROLE_NOT_GRANTED
    },
    "466": {
      "description": "Если срок действия токена истек",
      "schema": E_TOKEN_EXPIRED
    },
    "467": {
      "description": "Если токен имеет неверный формат",
      "schema": E_TOKEN_INVALID
    },
    "500": {
      "description": "В случае иных ошибок в процессе обработки данных, кроме перечисленных ранее",
      "schema": E_INTERNAL_ERROR
    }
  }
}


