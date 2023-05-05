from auth.docspecs.http_exceptions import (
  E_INTERNAL_ERROR,
  E_UNSUPPORTED_OAUTH_PROVIDER,
  E_RATE_LIMIT_EXCEEDED
)
from auth.docspecs.response_models import RESPONSE_BASE

R_OAUTH_PHASE1_SUCCESS = {**RESPONSE_BASE, **{
  "example": {
    "code": 200,
    "data": {
      "redirect": "https://oauth.yandex.ru/authorize?response_type=token&client_id=9cd85d5f9a5948f88f7c04ee99d4eb38&scope=login%3Aemail+login%3Ainfo&state=Nbfo080JEA5OCMsBz9sC7EPFLQ1fus"
    },
    "description": "see redirection url",
    "success": True
  }
}}


OAUTH = {
  "tags": [
    "Вход в систему через oauth-провайдеров (Yandex)"
  ],
  "description": """
  Вход через OAuth-авторизацию на сторонных серверах.
  Данный вызов вернет redirect URL, который надо вставить в браузер. После авторизации, 
  callback-ом потребителя является http://127.0.0.1/user/v1/oauth/[имя_провайдера]/callback,
  который (в случае подтверждения авторизации) вернет все необходимые авторизационны данные, которые
  можно использовать в дальшейших ручных тестах через openapi
  """,
  "parameters": [
    {
      "in": "path",
      "name": "service",
      "type": "string",
      "enum": [
        "yandex",
      ],
      "required": True,
      "default": "yandex"
    },
  ],
  "responses": {
    "200": {
      "description": "Провайдер поддерживается, URL для redirect сформирован и доступен в data",
      "schema": R_OAUTH_PHASE1_SUCCESS
    },
    "462": {
      "description": "Если **service** не является именем поддерживаемого провайдера OAuth2",
      "schema": E_UNSUPPORTED_OAUTH_PROVIDER
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


