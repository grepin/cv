from auth.docspecs.request_models import USER4UPDATE
from auth.docspecs.http_exceptions import (
  E_NO_ACCESS_TOKEN_SPECIFIED,
  RESPONSE_BASE,
  E_INTERNAL_ERROR,
  E_TOKEN_INVALID,
  E_TOKEN_EXPIRED,
  E_RATE_LIMIT_EXCEEDED,
  E_INPUT_VALIDATION_ERROR,
  E_ACCESS_TOKEN_REVOKED
)


R_UPDATE_SUCCESS = {**RESPONSE_BASE, **{
  "example": {
    "code": 200,
    "data": {
      "email": "adam@mankind.com",
      "lastname": "thefirstman",
      "login": "adam",
      "name": "adam"
    },
    "description": "user updated",
    "success": True
  }
}}


UPDATE = {
  "tags": [
    "Обновление сведений о пользователе"
  ],
  "description": """
  Для обновления логина, email, пароля, name или lastname (ID пользователя берется из access-токена)
  Могут указывается как все параметры, так и какое-то отдельное подмножество
  """,
  "security": [{"Bearer": []}],
  "parameters": [
    {
      "in": "body",
      "name": "payload",
      "schema": USER4UPDATE
    },
  ],
  "responses": {
    "200": {
      "description": "Успешное обновление, получение полной обновленной информации о пользователе",
      "schema": R_UPDATE_SUCCESS
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
    "452": {
      "description": "При отсутствии или любых несоответствиях формата входных данных",
      "schema": E_INPUT_VALIDATION_ERROR
    },
    "465": {
      "description": "Если превышено допустимое число запросов в единицу времени",
      "schema": E_RATE_LIMIT_EXCEEDED
    },
    "500": {
      "description": "В случае иных ошибок в процессе обработки данных, кроме перечисленных ранее",
      "schema": E_INTERNAL_ERROR
    }
  }
}




