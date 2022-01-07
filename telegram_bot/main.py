import logging

from aiogram import Dispatcher, executor, types
from aiogram.utils import exceptions
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import handlers
from settings import ADMIN_LIST, ACCESS_TOKEN_LIFETIME
from loader import auth, bot, dp

logging.basicConfig(level=logging.INFO)

scheduler = AsyncIOScheduler()


def schedule_jobs() -> None:
    """Queues that update access token."""
    scheduler.add_job(auth.refresh_token, 'interval', minutes=ACCESS_TOKEN_LIFETIME)


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
