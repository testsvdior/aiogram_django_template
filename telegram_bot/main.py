import logging

from aiogram import Bot, Dispatcher, executor, types

from requests import create_user_query, get_users_list, get_jwt_credentials
from settings import BOT_TOKEN
from utils import prepare_user_data, prepare_users_list


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
    user_data = message.from_user.to_python()
    prepared_data = await prepare_user_data(data=user_data)
    status = await create_user_query(data=prepared_data)
    assert status in (400, 201), status
    await message.answer(f"Your Telegram ID is <code>{message.chat.id}</code>\nHelp and source code: /help")


@dp.message_handler(commands='users')
async def cmd_users(message: types.Message):
    """
    This handler will be called when user sends `/users`
    :param message: Telegram message with "/users" command
    """
    data = await get_users_list()
    users = await prepare_users_list(data=data)
    await message.answer(text='\n'.join(users))


# todo - временное решение.
@dp.message_handler(commands='test')
async def cmd_users(message: types.Message):
    """
    This handler generate JWT.
    :param message: Telegram message with "/users" command
    """
    await get_jwt_credentials()
    await message.answer(text='testing')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
