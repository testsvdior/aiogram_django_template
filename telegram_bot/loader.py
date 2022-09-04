import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
import sentry_sdk

from auth import AuthBackend
from settings import RedisSettings, SENTRY_DSN, get_bot_config

bot_config = get_bot_config()

auth = AuthBackend()

storage = RedisStorage2(host=RedisSettings.host, port=RedisSettings.port, password=RedisSettings.password)

# Initialize bot and dispatcher
bot = Bot(token=bot_config.bot_token, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)

bot_commands = [
    types.BotCommand(command="/start", description="Register user."),
    types.BotCommand(command="/users", description="Show bot users."),
    types.BotCommand(command="/message", description="Send messages to all users."),
    types.BotCommand(command="/help", description="Help command."),
]


try:
    sentry_sdk.init(
        dsn=SENTRY_DSN,

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )
except Exception as e:
    logging.error(e)
    logging.info('Sentry not initialized')
