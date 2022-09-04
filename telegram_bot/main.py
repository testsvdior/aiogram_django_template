import logging

from aiogram import Dispatcher, executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import handlers  # need import if we want to register our handlers
from handlers.services import send_message
from settings import BackendSettings
from loader import auth, bot, dp, bot_commands, bot_config

logging.basicConfig(level=logging.INFO)

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")


def schedule_jobs() -> None:
    """Queues that update access token."""
    scheduler.add_job(auth.refresh_token, 'interval', minutes=BackendSettings.access_token_lifetime)


async def on_startup(dispatcher: Dispatcher) -> None:
    """
    Function starting on startup bot.
    :param dispatcher: aiogram.Dispatcher
    :return: None
    """
    await auth.auth_user()

    await bot.set_my_commands(bot_commands)
    for admin in bot_config.admin_list:
        await send_message(admin, message='Bot on startup.')
    schedule_jobs()


if __name__ == "__main__":
    scheduler.start()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
