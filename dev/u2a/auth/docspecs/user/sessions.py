from auth.docspecs.http_exceptions import (
  E_NO_SUCH_USER,
  E_INVALID_CREDENTIALS,
  E_MISSING_FIELD,
  E_NO_ACCESS_TOKEN_SPECIFIED,
  E_INTERNAL_ERROR,
  E_RATE_LIMIT_EXCEEDED,
  E_TOKEN_EXPIRED,
  E_TOKEN_INVALID,
  E_ACCESS_TOKEN_REVOKED
)
from auth.docspecs.response_models import RESPONSE_BASE

R_SESSIONS_SUCCESS = {**RESPONSE_BASE, **{
  "example": {
    "code": 200,
    "data": {
      "count": 3,
      "sessions": [
        {
          "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6MTY1NDg0OTE1OS44MjA3MjEsImlhdCI6MTY1NDg0OTEyOSwianRpIjoiYjU5NWNmZDgtNDhhMC00MTE3LTgyNTUtZjU0ZTJlYTgxMGE4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjE5Y2JiZWVmLWJiYjItNGZiZi05Y2U3LTY1NWFlNDcwZGNlNiIsIm5iZiI6MTY1NDg0OTEyOSwiZXhwIjoxNjU0ODQ5NDI5LCJuYW1lIjoiYWRhbSIsImlkIjoiMTljYmJlZWYtYmJiMi00ZmJmLTljZTctNjU1YWU0NzBkY2U2IiwibGFzdG5hbWUiOiJmaXJzdG1hbiIsImFjdGl2ZSI6MSwiZW1haWwiOiJhZGFtQG1hbmtpbmQuY29tIiwibG9naW4iOiJhZGFtIiwicm9sZXMiOnsidXNlciI6IjUxMjIzZjdiLTJiMDYtNDMzNy04YzViLTQxNDdjOGYzMzllMiJ9fQ.0dMKu3eA6zjIyBBYU639x5GBhK-y1p0raQvJxka9c_U",
          "expires": "2022-06-10T08:23:49.833368",
          "logon_date": "2022-06-10T08:18:49.816547"
        },
        {
          "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6MTY1NDg1MDE1Mi4yNTAyMywiaWF0IjoxNjU0ODUwMTIyLCJqdGkiOiI0YzEwMDEzMy0zZGE5LTQyNmYtYmI2ZS05NGUzMjViYzE4MTIiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiMTljYmJlZWYtYmJiMi00ZmJmLTljZTctNjU1YWU0NzBkY2U2IiwibmJmIjoxNjU0ODUwMTIyLCJleHAiOjE2NTQ4NTA0MjIsIm5hbWUiOiJhZGFtIiwibGFzdG5hbWUiOiJmaXJzdG1hbiIsImFjdGl2ZSI6MSwiZW1haWwiOiJhZGFtQG1hbmtpbmQuY29tIiwiaWQiOiIxOWNiYmVlZi1iYmIyLTRmYmYtOWNlNy02NTVhZTQ3MGRjZTYiLCJsb2dpbiI6ImFkYW0iLCJyb2xlcyI6eyJ1c2VyIjoiNTEyMjNmN2ItMmIwNi00MzM3LThjNWItNDE0N2M4ZjMzOWUyIn19.BbiRiDk50qCNCmlakJ6rTQLjXQxDUEG1ipjncc-pmTc",
          "expires": "2022-06-10T08:40:22.261538",
          "logon_date": "2022-06-10T08:35:22.239904"
        },
        {
          "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6MTY1NDg0OTc0MS4yODA1MDIsImlhdCI6MTY1NDg0OTcxMSwianRpIjoiMzVlMTIwZDgtY2MwOS00M2RlLTlkOWUtYTQzYTA4NzkyN2QwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjE5Y2JiZWVmLWJiYjItNGZiZi05Y2U3LTY1NWFlNDcwZGNlNiIsIm5iZiI6MTY1NDg0OTcxMSwiZXhwIjoxNjU0ODUwMDExLCJhY3RpdmUiOjEsImVtYWlsIjoiYWRhbUBtYW5raW5kLmNvbSIsIm5hbWUiOiJhZGFtIiwibG9naW4iOiJhZGFtIiwiaWQiOiIxOWNiYmVlZi1iYmIyLTRmYmYtOWNlNy02NTVhZTQ3MGRjZTYiLCJsYXN0bmFtZSI6ImZpcnN0bWFuIiwicm9sZXMiOnsidXNlciI6IjUxMjIzZjdiLTJiMDYtNDMzNy04YzViLTQxNDdjOGYzMzllMiJ9fQ.vBy67PK8BxhqRJS2F4iTpslFrsS4zzuP16NxoBRttw4",
          "expires": "2022-06-10T08:33:31.292054",
          "logon_date": "2022-06-10T08:28:31.265589"
        }
      ]
    },
    "description": "sessions retrieved",
    "success": True
  }
}}


SESSIONS = {
  "tags": [
    "Перечень пользовательских сессий"
  ],
  "security": [{"Bearer": []}],
  "description": """
  Получение перечня сессий, открытых пользователем
  """,
  "parameters": [
  ],
  "responses": {
    "200": {
      "description": "Успешное завершение, перечень сессий в поле data",
      "schema": R_SESSIONS_SUCCESS
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


