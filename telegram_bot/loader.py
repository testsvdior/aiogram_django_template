from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from auth import AuthBackend
from settings import BOT_TOKEN

auth = AuthBackend()

storage = MemoryStorage()

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)
