import os
from pathlib import Path
from typing import List

import environ

IS_DOCKER = os.environ.get("IS_DOCKER", False)

if IS_DOCKER:
    BOT_DIR = Path(__file__).resolve().parent
else:
    BOT_DIR = Path(__file__).resolve().parent.parent


# Initialize environ and get environments from .env file
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
)
environ.Env.read_env(BOT_DIR / '.env')

BOT_TOKEN: str = env('BOT_TOKEN')
ADMIN_LIST: List = env.list('ADMIN_LIST')

default_backend_value = "http://django:8000/" if IS_DOCKER else "http://localhost:8000/"
BACKEND_URL: str = env('BACKEND_URL', default=default_backend_value)

# authentication credentials
REQUEST_USER_LOGIN: str = env('ADMIN_USERNAME')
REQUEST_USER_PASSWORD: str = env('ADMIN_PASSWORD')

# JWT settings
ACCESS_TOKEN_LIFETIME: int = env.int('ACCESS_TOKEN_LIFETIME') - 1


# REDIS
REDIS_HOST: str = env('REDIS_HOST')
REDIS_PORT: int = env.int('REDIS_PORT')
REDIS_PASSWORD: str = env('REDIS_PASSWORD')
