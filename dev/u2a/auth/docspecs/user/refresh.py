from auth.docspecs.request_models import USER4REGISTER, AUTH_HEADER
from auth.docspecs.http_exceptions import (
  E_NO_ACCESS_TOKEN_SPECIFIED,
  E_REFRESH_TOKEN_NEEDED,
  RESPONSE_BASE,
  E_TOKEN_INVALID,
  E_INTERNAL_ERROR,
  E_TOKEN_EXPIRED,
  E_RATE_LIMIT_EXCEEDED,
  E_ACCESS_TOKEN_REVOKED
)

R_REFRESH_SUCCESS = {**RESPONSE_BASE, **{
  "example": {
    "code": 200,
    "data": {
      "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6MTY1MjY0NjEwNC4wNzE3MDIsImlhdCI6MTY1MjY0NjA3NCwianRpIjoiN2M1MTMzMWMtNGY0ZC00MTBiLTg4MzMtMjdhMzkzNzkwN2QwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjZjM2NkOGEwLThkNzUtNDVlMC1iZWI2LTkzMGVlNTEzYzY4NiIsIm5iZiI6MTY1MjY0NjA3NCwiZXhwIjoxNjUyNjQ2MTA0LCJsYXN0bmFtZSI6ImZpcnN0bWFuIiwiZW1haWwiOiJhZGFtQG1hbmtpbmQuY29tIiwiaWQiOiI2YzNjZDhhMC04ZDc1LTQ1ZTAtYmViNi05MzBlZTUxM2M2ODYiLCJuYW1lIjoiYWRhbSIsImFjdGl2ZSI6ZmFsc2UsImxvZ2luIjoiYWRhbSIsInJvbGVzIjp7InVzZXIiOiI4MjNjZTIyMy00OTIzLTQyYTktYjcwZS0yZjUxNzYzOGU5ZGUifX0.q-qbMT8mINd5R_IAEq21_R_dPYSTSqpxUwKoNjI5OXA",
      "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MjY0NjA3NCwianRpIjoiYWFlN2EzNTYtMjVlOS00MDU3LTllMjktY2MxYmE0NjY2ZTM3IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiI2YzNjZDhhMC04ZDc1LTQ1ZTAtYmViNi05MzBlZTUxM2M2ODYiLCJuYmYiOjE2NTI2NDYwNzQsImV4cCI6MTY1MjY0NjM3NCwibGFzdG5hbWUiOiJmaXJzdG1hbiIsImVtYWlsIjoiYWRhbUBtYW5raW5kLmNvbSIsImlkIjoiNmMzY2Q4YTAtOGQ3NS00NWUwLWJlYjYtOTMwZWU1MTNjNjg2IiwibmFtZSI6ImFkYW0iLCJhY3RpdmUiOmZhbHNlLCJsb2dpbiI6ImFkYW0iLCJyb2xlcyI6eyJ1c2VyIjoiODIzY2UyMjMtNDkyMy00MmE5LWI3MGUtMmY1MTc2MzhlOWRlIn19.KoDizMOZso_ZtNiGRoM2Vk8K_YbI7KdvKbj24mBI8QI"
    },
    "description": "tokens refreshed",
    "success": True
  }
}}

REFRESH = {
  "tags": [
    "Обновление токенов авторизации"
  ],
  "description": """
  Возвращает пару токенов (access, refresh) при условии, что refresh не истек.
  В заголовке авторизации ожидается refresh-токен
  """,
  "security": [{"Bearer": []}],
  "responses": {
    "200": {
      "description": "Получение пары обновленных токенов",
      "schema": R_REFRESH_SUCCESS
    },
    "440": {
      "description": "Если не указан refresh-токен в заголовке авторизации",
      "schema": E_NO_ACCESS_TOKEN_SPECIFIED
    },
    "456": {
      "description": "Если токен был отозван",
      "schema": E_ACCESS_TOKEN_REVOKED
    },
    "457": {
      "description": "Если в заголовке вместо refresh-токена находится access-токен",
      "schema": E_REFRESH_TOKEN_NEEDED
    },
    "466": {
      "description": "Если срок действия токена истек",
      "schema": E_TOKEN_EXPIRED
    },
    "467": {
      "description": "Если токен имеет неверный формат",
      "schema": E_TOKEN_INVALID
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