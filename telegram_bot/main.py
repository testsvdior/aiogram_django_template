import logging
from pathlib import Path

import environ
from aiogram import Bot, Dispatcher, executor, types

BOT_DIR = Path(__file__).resolve().parent

# Initialize environ and get BOT_TOKEN from .env file
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
)
environ.Env.read_env(BOT_DIR / '.env')
BOT_TOKEN = env('BOT_TOKEN')

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler(chat_type=types.ChatType.PRIVATE, commands="start")
async def cmd_start(message: types.Message):
    """
    This handler will be called when user sends `/start`
    :param message: Telegram message with "/start" command
    """
    await message.answer(f"Your Telegram ID is <code>{message.chat.id}</code>\nHelp and source code: /help")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
