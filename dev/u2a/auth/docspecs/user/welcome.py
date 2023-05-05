from auth.docspecs.http_exceptions import (
  E_NO_SUCH_USER,
  E_INVALID_CREDENTIALS,
  E_MISSING_FIELD,
  E_INTERNAL_ERROR,
  E_RATE_LIMIT_EXCEEDED,
)
from auth.docspecs.response_models import RESPONSE_BASE

R_WELCOME_SUCCESS = {**RESPONSE_BASE, **{
  "example": {
      "code": 200,
      "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6MTY1NDgzOTgyMy40NTQyMzYsImlhdCI6MTY1NDgzOTc5MywianRpIjoiMjU1ZDJmNGEtYzAwYS00MzZkLTliZjQtNzgxYmYyNTY5YTM2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjA5NTQzNjBmLThmY2ItNGJiMC1iYzFjLTVjOWIxNWI0ZDZkOCIsIm5iZiI6MTY1NDgzOTc5MywiZXhwIjoxNzQxMjM5NzkzLCJpZCI6IjA5NTQzNjBmLThmY2ItNGJiMC1iYzFjLTVjOWIxNWI0ZDZkOCIsImVtYWlsIjoiMDk1NDM2MGY4ZmNiNGJiMGJjMWM1YzliMTViNGQ2ZDhAYW5vbnltb3VzLmxvY2FsIiwibmFtZSI6IjA5NTQzNjBmOGZjYjRiYjBiYzFjNWM5YjE1YjRkNmQ4IiwibGFzdG5hbWUiOiIwOTU0MzYwZjhmY2I0YmIwYmMxYzVjOWIxNWI0ZDZkOCIsImxvZ2luIjoiMDk1NDM2MGY4ZmNiNGJiMGJjMWM1YzliMTViNGQ2ZDgiLCJhY3RpdmUiOjEsInJvbGVzIjp7ImFub255bW91cyI6IjE1MDk0NWYxLTI2YjUtNDhlYy04NTA2LWQzZGU4MjYwMDhjZiJ9fQ.H5NL81YAqyYXIKQu8lKNIB95pEa9Ncvf3eRhXma-zvg",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1NDgzOTc5MywianRpIjoiYmIxNTc4NTAtMGVjYi00MDVmLTliNDktMjRmOTg4ZTRjNzNmIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiIwOTU0MzYwZi04ZmNiLTRiYjAtYmMxYy01YzliMTViNGQ2ZDgiLCJuYmYiOjE2NTQ4Mzk3OTMsImV4cCI6MTc0MTIzOTc5MywiaWQiOiIwOTU0MzYwZi04ZmNiLTRiYjAtYmMxYy01YzliMTViNGQ2ZDgiLCJlbWFpbCI6IjA5NTQzNjBmOGZjYjRiYjBiYzFjNWM5YjE1YjRkNmQ4QGFub255bW91cy5sb2NhbCIsIm5hbWUiOiIwOTU0MzYwZjhmY2I0YmIwYmMxYzVjOWIxNWI0ZDZkOCIsImxhc3RuYW1lIjoiMDk1NDM2MGY4ZmNiNGJiMGJjMWM1YzliMTViNGQ2ZDgiLCJsb2dpbiI6IjA5NTQzNjBmOGZjYjRiYjBiYzFjNWM5YjE1YjRkNmQ4IiwiYWN0aXZlIjoxLCJyb2xlcyI6eyJhbm9ueW1vdXMiOiIxNTA5NDVmMS0yNmI1LTQ4ZWMtODUwNi1kM2RlODI2MDA4Y2YifX0.Iyy99fN8Ft_25iL5IFtJm3F-QGKkSnGkeATfuath-aQ"
      },
      "description": "authenticated successfully",
      "success": True
  }
}}


WELCOME = {
  "tags": [
    "Псевдо-вход для анонимных пользователей"
  ],
  "description": """
  Возвращает действующие токены с длительным временем жизни и ролью anonymous.
  Необходим в рамках общей концепции работы с анонимными пользователями
  """,
  "parameters": [
  ],
  "responses": {
    "200": {
      "description": "Успешный вход, получение пары токенов",
      "schema": R_WELCOME_SUCCESS
    },
    "465": {
      "description": "Если превышено допустимое число запросов в единицу времени",
      "schema": E_RATE_LIMIT_EXCEEDED
    },
    "500": {
      "description": "В случае иных ошибок в процессе обработки данных",
      "schema": E_INTERNAL_ERROR
    }
  }
}


