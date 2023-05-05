from auth.docspecs.http_exceptions import (
  E_NO_SUCH_USER,
  E_INVALID_CREDENTIALS,
  E_MISSING_FIELD,
  E_INTERNAL_ERROR,
  E_RATE_LIMIT_EXCEEDED
)
from auth.docspecs.request_models import USER4LOGIN
from auth.docspecs.response_models import RESPONSE_BASE

R_LOGIN_SUCCESS = {**RESPONSE_BASE, **{
  "example": {
    "code": 200,
    "data": {
      "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6MTY1MjYzOTY3OS44MTgxNzcsImlhdCI6MTY1MjYzOTY0OSwianRpIjoiNzFiYTA1YTctZTAyZC00ZDQwLTlhNWMtYThmMGVlOWVkMDZjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImQ5YWM5ZDJjLTk2OTgtNDkxOC1hYjRhLTJiMWI4MGZiNjAwNSIsIm5iZiI6MTY1MjYzOTY0OSwiZXhwIjoxNjUyNjM5Njc5LCJsb2dpbiI6ImFkYW0iLCJuYW1lIjoiYWRhbSIsImFjdGl2ZSI6ZmFsc2UsImlkIjoiZDlhYzlkMmMtOTY5OC00OTE4LWFiNGEtMmIxYjgwZmI2MDA1IiwibGFzdG5hbWUiOiJmaXJzdG1hbiIsImVtYWlsIjoiYWRhbUBtYW5raW5kLmNvbSIsInJvbGVzIjp7InVzZXIiOiIzODA3YmRjMy00MzliLTQ5NDEtYjQ1Ni01OGRhMGNiNTBlNTAifX0.7xnCFfwc844EQODRvTQ1GBpZMb0sNG3sHu9BzobYb-I",
      "active": False,
      "email": "adam@mankind.com",
      "id": "d9ac9d2c-9698-4918-ab4a-2b1b80fb6005",
      "lastname": "firstman",
      "login": "adam",
      "name": "adam",
      "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MjYzOTY0OSwianRpIjoiMGVlZWM1OWYtMjZkNS00OGM4LWExN2YtMmQ5YWE4MjdjNTMxIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiJkOWFjOWQyYy05Njk4LTQ5MTgtYWI0YS0yYjFiODBmYjYwMDUiLCJuYmYiOjE2NTI2Mzk2NDksImV4cCI6MTY1MjYzOTk0OSwibG9naW4iOiJhZGFtIiwibmFtZSI6ImFkYW0iLCJhY3RpdmUiOmZhbHNlLCJpZCI6ImQ5YWM5ZDJjLTk2OTgtNDkxOC1hYjRhLTJiMWI4MGZiNjAwNSIsImxhc3RuYW1lIjoiZmlyc3RtYW4iLCJlbWFpbCI6ImFkYW1AbWFua2luZC5jb20iLCJyb2xlcyI6eyJ1c2VyIjoiMzgwN2JkYzMtNDM5Yi00OTQxLWI0NTYtNThkYTBjYjUwZTUwIn19.z5uj36uJ81wS-Hic3d92Py0kDYbCDhdDY9oDWUrXjtk",
      "roles": {
        "user": "3807bdc3-439b-4941-b456-58da0cb50e50"
      }
    },
    "description": "authenticated successfully",
    "success": True
  }
}}


LOGIN = {
  "tags": [
    "Вход в систему для зарегистированных пользователей"
  ],
  "description": """
  Получение токенов авторизации (access, refresh) для зарегистрированного пользователя.
  Для входа передаются логин и пароль, полученные после регистирации        
  """,
  "parameters": [
    {
      "in": "body",
      "name": "payload",
      "schema": USER4LOGIN
    },
  ],
  "responses": {
    "200": {
      "description": "Успешный вход, получение пары токенов и полной информации о пользователе (включая роли)",
      "schema": R_LOGIN_SUCCESS
    },
    "450": {
      "description": "Если пользователь с таким логином не зарегистрирован",
      "schema": E_NO_SUCH_USER
    },
    "441": {
      "description": "Если  неверный пароль",
      "schema": E_INVALID_CREDENTIALS
    },
    "455": {
      "description": "Если отсутствует логин или пароль",
      "schema": E_MISSING_FIELD
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


