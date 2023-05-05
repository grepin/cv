from auth.docspecs.http_exceptions import (
  E_CONSTRAINTS_VALIDATION,
  E_INTERNAL_ERROR,
  E_RATE_LIMIT_EXCEEDED,
  E_NO_ACCESS_TOKEN_SPECIFIED,
  E_TOKEN_INVALID,
  E_TOKEN_EXPIRED,
  E_INSUFFICIENT_RIGHTS
)
from auth.docspecs.request_models import ROLE4CREATE, ROLE
from auth.docspecs.response_models import RESPONSE_BASE

R_ROLE_CREATE_SUCCESS = {**RESPONSE_BASE, **{
  "example": {
    "code": 200,
    "data": {
      "passerby": "f4d4797a-1cdd-406d-9917-c82419dca4d2"
    },
    "description": "role created",
    "success": True
  }
}}


ROLE_CREATE = {
  "tags": [
    "Создание роли"
  ],
  "security": [{"Bearer": []}],
  "description": """
  Создает в системе роль с новым именем
  Для получения данных, пользователь (идентифицируемый токеном) должен иметь роль administrator или editor
  """,
  "parameters": [
    {
      "in": "body",
      "name": "payload",
      "schema": ROLE4CREATE
    },
  ],
  "responses": {
    "200": {
      "description": "Успешно, роль была создана",
      "schema": R_ROLE_CREATE_SUCCESS
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
    "451": {
      "description": "Если роль с таким именем уже существует",
      "schema": E_CONSTRAINTS_VALIDATION
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


