Сервис аутитенфикации находиться в репозитарии
git@github.com:sagrityanin/Auth_sprint_2.git
В репозитарии git@github.com:sagrityanin/Async_API_sprint_2.git
находится сервис выдачи контента, который самостоятельно обрабатывает JWT-токены,
при действующем токене из него береться роль и по ней производиться выдача контента,
при недействительном токене выдается ответ про необходимость обновления токена.
При отсутсвии токена - контент выдается как "unsubscriber".

Для запуска проекта следует создать файл .env по образу env_example. 
Способ для запуск тестов можно посмотреть Makefile раздел Test. 
Работу модуля аутентификации и авторизации для пользоватей 
можно посмотреть через nginx - http://127.0.0.1:8068/auth/api/v1/
Интерфейс администраторов работает по url - http://127.0.0.1:8008/admin/api/v1/
        либо http://127.0.0.1:5005/admin/api/v1/

Captcha-контейнер работает по url - http://127.0.0.1:5050/captcha/api/v1 либо
        http://127.0.0.1:8068/captcha/api/v1
Recaptcha - http://127.0.0.1:8068/recaptcha/api/v1
либо http://127.0.0.1:5055/recaptcha/api/v1

Работать с эндпоинтами можно через nginx на прямую, например curl -X 'POST'
'http://127.0.0.1:8088/auth/api/v1/users/new_user'
-H 'accept: application/json'
-H 'Content-Type: application/json'
-d '{ "email": "my_user", "password": "my_password", "login": "" }'

При запуске в test режиме jaeger отключен и с auth-контейнером swagger может работать на прямую
http://127.0.0.1:5000/auth/api/v1/
 
ВАЖНО
При смене режимов запуска сервис аутитенфикации
ОБЯЗАТЕЛЬНО ребилдить auth и admin-образ.


Создание суперпользователя: docker-compose exec -it admin bash flask superuser create 
Удаление суперпользователя: docker-compose exec -it admin bash flask superuser delete

Логическая схема логики представлена https://drive.google.com/file/d/1_GFchJJ8mLO559e4j5W44AWvUtRgtCkf/view?usp=sharing

Структура модуля - https://www.figma.com/file/qfTKXg2ZHSnxOMG81bSIOc/authAPI?node-id=0%3A1

При интенсивном использовании тесов следует увеличить параметры RATE_LIMIT в .env-файле.
Для включения jaeger-трасировщика в auth.core.config.settings следует параметр
TRACER_ON устанавить в True.

Для заполнения таблицы users_logs 
- docker compose exec -it token-payload python3 partition/fill_users_logs.py

