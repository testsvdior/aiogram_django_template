from pathlib import Path
from typing import List

import environ

BOT_DIR = Path(__file__).resolve().parent


# Initialize environ and get environments from .env file
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
)
environ.Env.read_env(BOT_DIR / '.env')

BOT_TOKEN: str = env('BOT_TOKEN')
ADMIN_LIST: List = env.list('ADMIN_LIST')

# if we run with Docker we user env BACKEND_URL from docker-compose, else use default address.
BACKEND_URL: str = env('BACKEND_URL', default='http://localhost:8000/')

# authentication credentials
REQUEST_USER_LOGIN: str = env('REQUEST_USER_LOGIN')
REQUEST_USER_PASSWORD: str = env('REQUEST_USER_PASSWORD')

# JWT settings
ACCESS_TOKEN_LIFETIME: int = env.int('ACCESS_TOKEN_LIFETIME') - 1
