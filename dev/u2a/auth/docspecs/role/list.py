from auth.docspecs.http_exceptions import (
  E_NO_SUCH_USER,
  E_INTERNAL_ERROR,
  E_RATE_LIMIT_EXCEEDED,
  E_NO_ACCESS_TOKEN_SPECIFIED,
  E_TOKEN_INVALID,
  E_TOKEN_EXPIRED,
  E_INSUFFICIENT_RIGHTS
)
from auth.docspecs.request_models import ROLE
from auth.docspecs.response_models import RESPONSE_BASE

R_ROLE_LIST_SUCCESS = {**RESPONSE_BASE, **{
  "example": {
    "code": 200,
    "data": {
      "administrator": "0a7c7482-ff98-4a4a-b4dc-a7c6075c8c17",
      "anonymous": "2bf8c364-7918-4fef-a9bb-ae1182660279",
      "editor": "572fdbe3-17e3-480b-83f2-cef9333aa6d1",
      "service": "21a0bbc5-63c0-4d56-a5ef-452c43e250c1",
      "subscriber": "9744d299-abc6-48a9-8862-0357cd4355a9",
      "user": "bf63a7a4-3847-4cc7-8a01-7d7db34f9301"
    },
    "description": "roles listed",
    "success": True
  }
}}


ROLE_LIST = {
  "tags": [
    "Перечень существующих ролей в системе"
  ],
  "security": [{"Bearer": []}],
  "description": """
  Возвращает перечень текстовых наименований ролей в системе с их идентификаторами.
  Для получения данных, пользователь (идентифицируемый токеном) должен иметь роль administrator или editor
  """,
  "parameters": [
  ],
  "responses": {
    "200": {
      "description": "Успешно, получение списка наименований и идентификаторов ролей",
      "schema": R_ROLE_LIST_SUCCESS
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


