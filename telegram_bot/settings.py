from pathlib import Path

import environ

BOT_DIR = Path(__file__).resolve().parent


# Initialize environ and get BOT_TOKEN from .env file
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
)
environ.Env.read_env(BOT_DIR / '.env')
BOT_TOKEN = env('BOT_TOKEN')


BACKEND_URL = 'http://localhost:8000/'

# authentication credentials
REQUEST_USER_LOGIN: str = env('REQUEST_USER_LOGIN')
REQUEST_USER_PASSWORD: str = env('REQUEST_USER_PASSWORD')
