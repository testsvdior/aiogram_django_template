from pathlib import Path
from typing import List, Union
from dataclasses import dataclass

import environ

ENV_DIR = Path(__file__).resolve().parent.parent


# Initialize environ and get environments from .env file
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
)
environ.Env.read_env(ENV_DIR / '.env')


# ADMIN_LIST: List = env.list('ADMIN_LIST')


@dataclass(frozen=True)
class BotSettings:
    """Bot settings."""
    bot_token: str
    admin_list: List[Union[str, int]]

    def __post_init__(self):
        self.validate_admin_list()

    def validate_admin_list(self):
        """Method check that admin ids contain only digits."""
        for admin_id in self.admin_list:
            if not admin_id.isdigit():
                raise ValueError(f'Admin id must contain only digits. Got {admin_id}')


@dataclass(frozen=True)
class BackendSettings:
    """Backend settings."""
    url: str = env('BACKEND_URL', default="http://django/")
    username: str = env('ADMIN_USERNAME')
    password: str = env('ADMIN_PASSWORD')
    # JWT token lifetime in minutes
    access_token_lifetime: int = env.int('ACCESS_TOKEN_LIFETIME') - 1


@dataclass(frozen=True)
class RedisSettings:
    host: str = env('REDIS_HOST')
    port: int = env.int('REDIS_PORT')
    password: str = env('REDIS_PASSWORD')


# SENTRY
SENTRY_DSN: str = env('SENTRY_DSN_TELEGRAM')


def get_bot_config() -> BotSettings:
    return BotSettings(
        bot_token=env('BOT_TOKEN'),
        admin_list=env.list('ADMIN_LIST'),
    )
