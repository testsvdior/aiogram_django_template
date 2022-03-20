import logging
from asyncio import sleep
from typing import Dict, Tuple

from aiogram import types
from aiogram.utils import exceptions
from aiogram.dispatcher import FSMContext

from handlers.exceptions import CommandArgumentError
from keyboards.inline import get_paginate_keyboard
from requests import get_user_detail_query, get_users_query
from utils import prepare_user_detail, prepare_users_list


async def get_detail_info(user_id: str) -> Tuple[str, bool]:
    """Function return user detail data."""
    if not user_id.isdigit():
        raise CommandArgumentError
    result = await get_user_detail_query(user_id=user_id)
    answer, is_banned = await prepare_user_detail(result)
    return answer, is_banned


async def send_message(user_id: int, message: types.Message) -> bool:
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


async def send_users(message: types.Message, state: FSMContext, payload: Dict = None):
    """
    Function return users-list from Backend.
    Function set state 'paginate' for user.

    :param message: Telegram message.
    :param state: state that we create to user.
    :param payload: data for paginate users-list.
    """
    state_data: Dict = await state.get_data()
    data = await get_users_query(payload=payload)
    if data['count'] == 0:
        await message.answer('We don\'t have any users.')
    else:
        users = await prepare_users_list(data=data['results'])
        message_data = {
            'text': '\n'.join(users),
            'reply_markup': await get_paginate_keyboard(next_page=data['next'], previous_page=data['previous']),
        }
        if state_data.get('edit', False):
            await message.edit_text(**message_data)
        else:
            await message.answer(f'Count of users: {data["count"]}')
            await message.answer(**message_data)
        await state.set_data({'edit': True})
        await state.set_state('paginate')
