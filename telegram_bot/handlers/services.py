import logging
from asyncio import sleep

from aiogram import types
from aiogram.utils import exceptions

from handlers.exceptions import CommandArgumentError
from requests import get_user_detail
from utils import prepare_user_detail


async def get_detail_info(user_id: str):
    """Function return user detail data."""
    if not user_id.isdigit():
        raise CommandArgumentError
    result = await get_user_detail(user_id=user_id)
    answer = await prepare_user_detail(result)
    return answer


async def send_message(user_id: int, message: types.Message):
    """
    Function send message message copy to Telegram bot user.
    :param user_id: ID of Telegram user.
    :param message: aiogram.types.Message that we will send to user.
    """
    try:
        await message.send_copy(user_id)
    except exceptions.BotBlocked:
        logging.error(f"Target [ID:{user_id}]: blocked by user")

    except exceptions.ChatNotFound:
        logging.error(f"Target [ID:{user_id}]: invalid user ID")

    except exceptions.RetryAfter as e:
        logging.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await sleep(e.timeout)
        return await send_message(user_id, message)

    except exceptions.UserDeactivated:
        logging.error(f"Target [ID:{user_id}]: user is deactivated")

    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{user_id}]: failed")

    else:
        logging.info(f"Target [ID:{user_id}]: success")
        return True

    return False
