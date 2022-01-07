from aiogram import Bot, Dispatcher


from auth import AuthBackend
from settings import BOT_TOKEN

auth = AuthBackend()

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)
