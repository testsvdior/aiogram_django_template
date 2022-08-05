from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from auth import AuthBackend
from settings import BOT_TOKEN, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

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
