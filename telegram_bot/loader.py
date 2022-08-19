from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
import sentry_sdk

from auth import AuthBackend
from settings import BOT_TOKEN, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, SENTRY_DSN

auth = AuthBackend()

storage = RedisStorage2(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)

bot_commands = [
    types.BotCommand(command="/start", description="Register user."),
    types.BotCommand(command="/users", description="Show bot users."),
    types.BotCommand(command="/message", description="Send messages to all users."),
    types.BotCommand(command="/help", description="Help command."),
]


sentry_sdk.init(
    dsn=SENTRY_DSN,

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)
