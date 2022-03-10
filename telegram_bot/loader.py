from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from auth import AuthBackend
from settings import BOT_TOKEN

auth = AuthBackend()

storage = MemoryStorage()

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)

bot_commands = [
    types.BotCommand(command="/start", description="Register user."),
    types.BotCommand(command="/users", description="Show bot users."),
    types.BotCommand(command="/message", description="Send messages to all users."),
    types.BotCommand(command="/help", description="Help command."),
]
