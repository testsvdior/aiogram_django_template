import logging

from aiogram import Bot, Dispatcher, executor, types

from requests import create_user_query
from settings import BOT_TOKEN

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
    user_data = message.from_user
    await create_user_query(data=user_data.to_python())
    await message.answer(f"Your Telegram ID is <code>{message.chat.id}</code>\nHelp and source code: /help")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
