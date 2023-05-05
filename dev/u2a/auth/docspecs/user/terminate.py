from auth.docspecs.http_exceptions import (
  E_NO_ACCESS_TOKEN_SPECIFIED,
  E_INTERNAL_ERROR,
  E_RATE_LIMIT_EXCEEDED,
  E_TOKEN_EXPIRED,
  E_TOKEN_INVALID,
  E_ACCESS_TOKEN_REVOKED
)
from auth.docspecs.response_models import RESPONSE_BASE

R_TERMINATE_SUCCESS = {**RESPONSE_BASE, **{
  "example": {
    "code": 200,
    "data": {},
    "description": "all sessions terminated",
    "success": False
  }
}}


TERMINATE = {
  "tags": [
    "Терминирование всех сессий пользователя"
  ],
  "security": [{"Bearer": []}],
  "description": """
  Инвалидирует все действиующие токены пользователя (включая анонимных)
  """,
  "parameters": [
  ],
  "responses": {
    "200": {
      "description": "Успешный выход, инвалидация всех токенов",
      "schema": R_TERMINATE_SUCCESS
    },
    "465": {
      "description": "Если превышено допустимое число запросов в единицу времени",
      "schema": E_RATE_LIMIT_EXCEEDED
    },
    "440": {
      "description": "Если не указан access-токен в заголовке авторизации",
      "schema": E_NO_ACCESS_TOKEN_SPECIFIED
    },
    "456": {
      "description": "Если токен был отозван",
      "schema": E_ACCESS_TOKEN_REVOKED
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
      "description": "В случае иных ошибок в процессе обработки данных",
      "schema": E_INTERNAL_ERROR
    }
  }
}


