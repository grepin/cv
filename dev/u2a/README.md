# Сервисы (Admin, ETL, search API, Auth) сквозного проекта в рамках Yandex.Practicum // Middle python developer
 - Admin: штатный [django-admin-app](/dev/u2a/app/app/movies/admin.py) с набором [моделей](/dev/u2a/app/app/movies/models.py)
 - ETL: программное [batch-извлечение](/dev/u2a/etl/etl/extractor.py) измененных данных из PostgeSQL с [трансформацией](/dev/u2a/etl/etl/transformer.py) и [загрузкой](/dev/u2a/etl/etl/loader.py) в ElasticSearch
 - Search API: FastAPI-based [API](/dev/u2a/api/api/v1) с поиском [фильмов](/dev/u2a/api/core/elastic_queries_films.py) и [персон](/dev/u2a/api/core/elastic_queries_persons.py) в ElasticSearch
 - Auth: [Flask-app](/dev/u2a/auth/app.py) для работы через [JWT](/dev/u2a/auth/extensions/jwt.py) с поддержкой дополнительного входа по [OAuth](/dev/u2a/auth/extensions/oauth.py)
 - OpenAPI docs для ручных тестов (при запущенной инфраструктуре): 
   - http://127.0.0.1:5000/auth/openapi
   - http://127.0.0.1:8000/api/openapi
   - [Auth-doc](/dev/u2a/auth/docspecs) спецификации [рендерятся для routes](/dev/u2a/auth/routes) через [Flassger](/dev/u2a/auth/extensions/flassger.py) по OpenAPI 2.0, поэтому для ручных тестов через OpenAPI-интерфейс необходимо при вводе 
    токена в поле Authorization добавлять "Bearer " (с пробелом) вручную перед токеном (в 2.0 плохо со схемами)
 - В качестве внешнего OAuth-сервиса используется Yandex:
    - Схема стандартна: [основной вызов](/dev/u2a/auth/routes/user.py#L44),
      возвращающий ссылку для перенаправления (предполагается, что фронт выполнит обработку самостоятельно) и
      обработчик, который вызывает [сервисный callback-обработчик](/dev/u2a/auth/services/user.py#L107), 
      получающий от реализации обработки OAuth-callbacka из [соответствующего расширения
      данные о логине и email пользователя](/dev/u2a/auth/extensions/oauth.py#L96). Из особенностей - принципиально не использовал **state**, т.к. **code** Yandex делает
      одноразовым (большинство провайдеров делают так же, что вполне разумно)
    - Протестировать вход можно через OpenAPI, скопировав ссылку и перейдя по ней, а после чего - используя токены, 
     полученные в результате авторизации.
    - Для цели различия OAuth-аккаунта от системы авторизации [были добавлены](/dev/u2a/auth/utils/functional.py#L17) и
      [используются](/dev/u2a/auth/services/user.py#L121) **различные статусы активации**, на основании которых можно всегда отличить "родных"
      пользователей от OAuth-пользователей, что дает возможность в перспективе реализовать открепление
 - Интеграция:
    - базовая интеграция - через OpenAPI specification
    - GRPC-интеграция Auth и API:
        - [protobuf-схема](/dev/u2a/auth/grpcs/user.proto) описывает данные и метод whois, возвращающий по JWT-токену строковый список ролей
        - [сгенерированы](/dev/u2a/auth/grpcs/codegen.sh) две файла: [описания взаимодействия](/dev/u2a/auth/grpcs/user_pb2.py) и [функций сервера и клиента](/dev/u2a/auth/grpcs/user_pb2_grpc.py)
        - реализованный standalone-сервер на стороне auth-сервиса [использует flask app в качестве функционального контейнера](/dev/u2a/auth/grpc_server.py#L14),
        вызывая [соответствующий сервисный метод](/dev/u2a/auth/services/user.py#L226), который распаковывает токен и возвращает список ролей (метод интеграционный и не имеет внешнего HTTP API).
        - общий подход со стороны сервера: "при любой ошибке на стороне сервера, вернуть anonymous, как единственную роль"
        - в процесс ETL внесены изменения для обеспечения интеграции с клиентской стороны: все фильмы с известным рейтингом более 8.0 [маркируются](/dev/u2a/etl/etl/transformer.py#L9) как имеющие **subscription** (уровень подписки) равный 1 
        - на стороне клиента (в сервисе API) реализован GRPC-клиент с методом [whois](/dev/u2a/api/db/grpc.py#L22) для получения списка ролей по токену от Auth-сервиса и **circuit breaker** для этого метода (на базе пакета **lasier**)
        - общий подход со стороны клиента: "при любой ошибке удаленного вызова, вернуть anonymous как единственную роль"
        - Сервис авторизации клеинтской стороны [AuthService](/dev/u2a/api/services/auth.py#L6), отвечающий за [сопоставление roles и subscription](/dev/u2a/api/services/utils.py#L7) вызывается в момент, когда пользователь запрашивает [подробную информацию о кинопроизведении](/dev/u2a/api/api/v1/films.py#L72). 
          Таким образом, пользователи с подпиской смогут увидеть детальную информацию о фильмах с рейтингом более 8.0, а остальные - нет.           
  - Распределенная трассировка 
    - X-Request-Id формируется [nginx](/dev/u2a/auth/nginx.conf#L45), а для dev-режима (и соместимости с flask-cli) [генерируется динамически](/dev/u2a/auth/extensions/jaeger.py#L39) (что дает различные request id для вложенных спанов, но не является проблемой для dev-mode или cli)
    - Для трассировки используется сочетание [FlaskIntrumentor и дополнительного трассировщика](/dev/u2a/auth/extensions/jaeger.py#L54) с общим именем сервиса [auth](/dev/u2a/auth/extensions/jaeger.py#L20)
    - Трассировщик обернут в [декоратор](/dev/u2a/auth/extensions/jaeger.py#L71), которым оформлены транзитный вызов [handle](/dev/u2a/auth/utils/functional.py#L55) и сервисные вызовы Auth-сервиса, например: [login](/dev/u2a/auth/services/user.py#L87), [grant](/dev/u2a/auth/services/role.py#L50) и т.д.
  - RateLimiter 
    - [rate limiter](/dev/u2a/auth/extensions/ratelimiter.py#L19) релизован на базе пакета pyrate-limiter с использованием redis, как средства хранения данных
    - ключом служит [соединение ip-адреса (или X-Forwarded-For) и User-Agent](/dev/u2a/auth/extensions/ratelimiter.py#L13)
  - Партиционирование (Auth)
    - Партиционирование для Sessions реализовано как [HASH(user_id, id)](/dev/u2a/auth/models/models.py#L50), т.к. просто user_id не может быть уникальным ключом,
    но, при этом, мы должны обеспечить механику выбора сессий по user_id в партиционированной таблице
    - Для alembic (как основы используемого Flask-migrate) в миграцию [добавлены соответствующие дополнения по созданию таблиц-разделов](/dev/u2a/auth/migrations/versions/f7c2889735d8_initial.py#L38)

# Запуск
   - Предварительно создание .env:
```shell
  cp .env.sample .env
  cp tests/auth/functional/.env.sample tests/auth/functional/.env
```
   - Локальная инфраструктура разработки (минимальный набор, требуется запуск auth-сервиса, grpc-сервиса и api-сервиса через PyCharm/Консоль):
```shell
 docker-compose up 
 cd ./auth/
 ./migration-upgrade.sh
 ./migration-seed-roles.sh
 
```
   - Локальное функциональное тестирование (при минимальной инфраструктуре и запущенных приложениях):
```shell
  pytest tests/auth/functional
  pytest tests/api/functional
```
   - Полностью докерезированная инфраструктура приложения:
```shell
 docker-compose -f ./docker-compose.all.yml up 
```
   - Докерезированные тесты (при запущенной докерезированной инфраструктуре приложения):
```shell
 docker-compose -f ./tests/auth/functional/docker-compose.functional-tests-in-docker.yml  up 
 docker-compose -f ./tests/api/functional/docker-compose.functional-tests-in-docker.yml  up 
```

