# Aiogram and Django.

### Телеграм бот на асинхронной библиотеке Aiogram который подключается с помощью Aiohttp к REST написанный на Django.



#### Запуск проекта с помощью Docker:

1. Переименуйте файл `telegram_bot/.env.dist` на `.env` можно использовать команду `mv telegram_bot/.env.dist telegram_bot/.env`

2. Заполните следующие поля в файле `.env` : 

   - **BOT_TOKEN** - это токен Telegram бота.

   - **REQUEST_USER_LOGIN** - это имя суперпользователя Django.

   - **REQUEST_USER_PASSWORD** - пароль суперпользователя Django.

   - **ADMIN_LIST** - id пользователей владельца/модераторов бота, пишем через запятую.

   - **ACCESS_TOKEN_LIFETIME** - время жизни access_token который используется для подключения к REST на Django.

     *(REQUEST_USER_LOGIN, REQUEST_USER_PASSWORD, ACCESS_TOKEN_LIFETIME) - можне не трогать.*

3. `make build` или `docker-compose build && docker-compose up`

4. Если на id пользователей которых вы указали в переменной ADMIN_LIST придет сообщение то проект успешно запущен!

   (На ID пользователей не придет уведомление если они не нажимали в вашем боте команду `/start`).



#### Зависимости проекта:

JWT аутентификация - https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html  
Swagger - https://drf-spectacular.readthedocs.io/en/latest/
