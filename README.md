Для запуска приложения:

1. Заполнить поля настроек, если потребуется, в файле `.env-example` -> удалить суффикс `example`
2. Установить Docker и создать нужные образы с помощью команды `docker-compose -f docker-compose-dev-example.yml up --build`.
   2.1. При скачивании образа elasticsearch, возможно, потребуется подключение к vpn.
3. Перейти по адресу `http://localhost/api/openapi`

Для запуска автотестов:

1. Перенести настройки из `.env-example-tests` в `.env`
2. Установить Docker -> ввести команду `docker-compose -f api_service/tests/functional/docker-compose.yml up --build`
3. Директория тестов: `api_service/tests`
