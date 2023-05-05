from auth.docspecs.request_models import USER4REGISTER
from auth.docspecs.http_exceptions import (
  E_CONSTRAINTS_VALIDATION,
  RESPONSE_BASE,
  E_INPUT_VALIDATION_ERROR,
  E_INTERNAL_ERROR,
  E_RATE_LIMIT_EXCEEDED
)

R_REGISTER_SUCCESS = {**RESPONSE_BASE, **{
  "example": {
    "code": 200,
    "data": {
      "active": False,
      "email": "adam@mankind.com",
      "id": "7c466fab-6f61-431c-9e87-bbf886a2a4ab",
      "lastname": "firstman",
      "login": "adam",
      "name": "adam",
      "roles": {
        "user": "bff4b063-6897-4126-9ab5-fa3457dc0384"
      }
    },
    "description": "user registered",
    "success": True
  }
}}

REGISTER = {
  "tags": [
    "Регистрация нового пользователя в системе"
  ],
  "description": """
  Регистрация нового пользователя с присвоением роли **user**. Поля **name** и **lastname** - необязательные
  """,
  "parameters": [
    {
      "in": "body",
      "name": "payload",
      "schema": USER4REGISTER
    },
  ],
  "responses": {
    "200": {
      "description": "Успешный вход, получение всех сведений о созданном пользователе в data",
      "schema": R_REGISTER_SUCCESS
    },
    "451": {
      "description": "Если пользователь с таким логином или email уже зарегистрирован",
      "schema": E_CONSTRAINTS_VALIDATION
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