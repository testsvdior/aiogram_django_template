from aiogram import types
from aiogram.utils import exceptions

from loader import dp
from requests import get_users_list, get_user_detail
from utils import prepare_users_list, prepare_user_detail


@dp.message_handler(commands='users')
async def cmd_users(message: types.Message):
    """
    This handler will be called when user sends `/users`
    :param message: Telegram message with "/users" command
    """
    data = await get_users_list()
    users = await prepare_users_list(data=data)
    await message.answer(text='\n'.join(users))


@dp.message_handler(commands='detail')
async def user_detail(message: types.Message):
    try:
        arguments: str = message.get_args()
        result = await get_user_detail(user_id=arguments)
        answer = await prepare_user_detail(result)
        await message.reply(answer)
    except exceptions.MessageTextIsEmpty:
        await message.answer("You didn't send user id!")
