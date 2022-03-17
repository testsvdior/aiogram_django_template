import logging

from aiogram import Dispatcher, executor
from aiogram.utils import exceptions
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import handlers  # need import if we want to register our handlers
from settings import ADMIN_LIST, ACCESS_TOKEN_LIFETIME
from loader import auth, bot, dp, bot_commands

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

    await bot.set_my_commands(bot_commands)
    for admin in ADMIN_LIST:
        try:
            await bot.send_message(chat_id=admin, text='Bot on startup.', )
        except exceptions.ChatNotFound as e:
            logging.error(f'Can not send message to admin with ID {admin}. Exception: {e}')
    schedule_jobs()


if __name__ == "__main__":
    scheduler.start()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
