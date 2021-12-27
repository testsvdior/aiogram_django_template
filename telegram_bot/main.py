import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils import exceptions
from apscheduler.schedulers.asyncio import AsyncIOScheduler


from requests import create_user_query, get_users_list
from settings import BOT_TOKEN, ADMIN_LIST, ACCESS_TOKEN_LIFETIME
from utils import prepare_user_data, prepare_users_list
from loader import auth

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

scheduler = AsyncIOScheduler()


def schedule_jobs() -> None:
    """Queues that update access token."""
    scheduler.add_job(auth.refresh_token, 'interval', minutes=ACCESS_TOKEN_LIFETIME)


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


async def on_startup(dispatcher: Dispatcher) -> None:
    """
    Function starting on startup bot.
    :param dispatcher: aiogram.Dispatcher
    :return: None
    """
    await auth.auth_user()
    bot_commands = [
        types.BotCommand(command="/start", description="Register,"),
        types.BotCommand(command="/users", description="Show bot users."),
    ]
    await bot.set_my_commands(bot_commands)
    for admin in ADMIN_LIST:
        try:
            await bot.send_message(chat_id=admin, text='Bot on startup.', )
        except exceptions.ChatNotFound as e:
            # todo - create logger that write exception to file.
            print(f'{admin} {e}'.lower())
    schedule_jobs()


if __name__ == "__main__":
    scheduler.start()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
