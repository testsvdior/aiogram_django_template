from aiogram import types

from loader import dp
from requests import create_user_query
from utils import prepare_user_data


@dp.message_handler(chat_type=types.ChatType.PRIVATE, commands="start")
async def cmd_start(message: types.Message):
    """
    This handler will be called when user sends `/start`
    :param message: Telegram message with "/start" command
    """
    user_data = message.from_user.to_python()
    prepared_data = await prepare_user_data(data=user_data)
    status = await create_user_query(data=prepared_data)
    assert status in (400, 201), status
    await message.answer(f"Your Telegram ID is <code>{message.chat.id}</code>\nHelp and source code: /help")
