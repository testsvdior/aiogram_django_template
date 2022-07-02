# Django-Aiogram Template.

### Template stack:

1) **Django** - to admin project.
2) **Aiogram** - to connect Telegram BOT API. Using **Aiohttp** client for connect to django service.
3) ***Gunicorn**
4) ***Nginx**
5) ***Postgres**
6) ***Docker/docker-compose**

## Setup project with Docker

1) #### Change enviroments

   - Rename `.env.dist` to `.env`
   - Update default values from `.env`

2) #### Build project

   ```shell
   docker-compose -f docker-compose.prod.yaml build
   ```

3) #### Up project

   ```shell
   docker-compose -f docker-compose.prod.yaml up -d
   ```

#### Third-party project dependencies:

JWT authentification - https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html  
Swagger generation - https://drf-spectacular.readthedocs.io/en/latest/

