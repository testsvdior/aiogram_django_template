from typing import Dict

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import exceptions

from loader import dp
from requests import get_users_data, get_user_detail
from utils import prepare_users_list, prepare_user_detail
from settings import ADMIN_LIST
from handlers.exceptions import CommandArgumentError
from keyboards.inline import get_paginate_keyboard


async def send_users(message: types.Message, state: FSMContext, payload: Dict = None):
    """
    Function return users-list from Backend.
    Function set state 'paginate' for user.

    :param message: Telegram message.
    :param state: state that we create to user.
    :param payload: data for paginate users-list.
    """
    state_data: Dict = await state.get_data()
    data = await get_users_data(payload=payload)
    if data['count'] == 0:
        await message.answer('We don\'t have any users.')
    else:
        users = await prepare_users_list(data=data['results'])
        message_data = {
            'text': '\n'.join(users),
            'reply_markup': get_paginate_keyboard(next_page=data['next'], previous_page=data['previous']),
        }
        if state_data.get('edit', False):
            await message.edit_text(**message_data)
        else:
            await message.answer(f'Count of users: {data["count"]}')
            await message.answer(**message_data)
        # write message ID to state data
        await state.set_data({'edit': True})
        await state.set_state('paginate')


@dp.message_handler(commands='users', user_id=ADMIN_LIST)
async def cmd_users(message: types.Message, state: FSMContext):
    """
    This handler will be called when user sends `/users`
    :param message: Telegram message with "/users" command.
    :param state: state that we create to user.
    """
    await send_users(message, state=state)


@dp.callback_query_handler(lambda c: c.data.startswith('page'), state='paginate')
async def users_paginate(call: types.CallbackQuery, state: FSMContext):
    """
    This handler will be called when user touch inline keyboards from message with paginate.
    :param call: Telegram callback query with data that startswith "page".
    :param state: state that we create to user.
    """
    page = call.data.split('=')[1]
    if page.isdigit():
        await send_users(call.message, state=state, payload={'p': page})
    else:
        await call.answer('Inactive keyboard')


@dp.callback_query_handler(lambda c: c.data == 'exit', state='*')
async def exit_from_state(call: types.CallbackQuery, state: FSMContext):
    """Function exit user from any state.
    :param call: Telegram callback query with data "exit".
    :param state: state.
    """
    await state.finish()
    await call.message.delete_reply_markup()
    await call.answer('You are exit from state')


@dp.message_handler(commands='detail', user_id=ADMIN_LIST)
async def cmd_user_detail(message: types.Message):
    """
    Handler return user detail info.
    Example:
        "/detail 111222333" - will return info about user with ID 11122333

    :param message: message with command from Telegram.
    """
    try:
        argument: str = message.get_args()
        if not argument.isdigit():
            raise CommandArgumentError
        result = await get_user_detail(user_id=argument)
        answer = await prepare_user_detail(result)
        await message.reply(answer)
    except exceptions.MessageTextIsEmpty:
        await message.answer("You didn't send user id!")
    except CommandArgumentError:
        await message.answer('ID must contains only digits.')
