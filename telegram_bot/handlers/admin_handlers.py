from aiogram import types

from loader import dp
from requests import get_users_list
from utils import prepare_users_list


@dp.message_handler(commands='users')
async def cmd_users(message: types.Message):
    """
    This handler will be called when user sends `/users`
    :param message: Telegram message with "/users" command
    """
    data = await get_users_list()
    users = await prepare_users_list(data=data)
    await message.answer(text='\n'.join(users))
