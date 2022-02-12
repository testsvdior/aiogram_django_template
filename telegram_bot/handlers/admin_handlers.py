from typing import Dict
from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import exceptions

from handlers.services import get_detail_info, send_message
from loader import dp, bot
from requests import get_users
from utils import prepare_users_list
from settings import ADMIN_LIST
from handlers.exceptions import CommandArgumentError, NotFound
from keyboards.inline import get_paginate_keyboard, get_exit_keyboard


async def send_users(message: types.Message, state: FSMContext, payload: Dict = None):
    """
    Function return users-list from Backend.
    Function set state 'paginate' for user.

    :param message: Telegram message.
    :param state: state that we create to user.
    :param payload: data for paginate users-list.
    """
    state_data: Dict = await state.get_data()
    data = await get_users(payload=payload)
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


@dp.message_handler(commands='users', user_id=ADMIN_LIST)
async def cmd_users(message: types.Message, state: FSMContext):
    """
    This handler will be called when user sends `/users`
    :param message: Telegram message with "/users" command.
    :param state: state that we create to user.
    """
    await send_users(message, state=state, payload={'page_size': 10, 'p': 1})


@dp.callback_query_handler(lambda c: c.data.startswith('page'), state='paginate')
async def users_paginate(call: types.CallbackQuery, state: FSMContext):
    """
    This handler will be called when user touch inline keyboards from message with paginate.
    :param call: Telegram callback query with data that startswith "page".
    :param state: state that we create to user.
    """
    page = call.data.split('=')[1]
    if page.isdigit():
        await send_users(call.message, state=state, payload={'page_size': 10, 'p': page})
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
    await sleep(1)
    await call.message.delete()


@dp.message_handler(lambda m: m.text.startswith('/'), state='paginate')
@dp.message_handler(commands='detail', user_id=ADMIN_LIST)
async def cmd_user_detail(message: types.Message):
    """
    Handler return user detail info.
    Example:
        "/detail 111222333" - will return info about user with ID 11122333
        "/111222333" will work when admin click on the state paginate

    :param message: message with command from Telegram.
    """
    try:
        if message.text[1:].isdigit():
            user_id = message.text[1:]
        else:
            user_id: str = message.get_args()
        answer = await get_detail_info(user_id=user_id)
        await message.answer(answer, reply_markup=await get_exit_keyboard())
    except exceptions.MessageTextIsEmpty:
        await message.answer("You didn't send user id!")
    except CommandArgumentError:
        await message.answer('ID must contains only digits.')
    except NotFound:
        await message.answer('User was not found.')


@dp.message_handler(commands='message', user_id=ADMIN_LIST)
async def cmd_message(message: types.Message, state: FSMContext) -> None:
    answer = [
        'Send me message, that you want to send users.',
        'To cancel click the button below',
    ]
    await message.answer('\n'.join(answer), reply_markup=await get_exit_keyboard())
    await state.set_state('message')


@dp.message_handler(state='message')
async def state_message(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Starting to send messages.')
    users_data = await get_users(payload={'only_id': 1})
    count = 0
    for user in users_data:
        if await send_message(user_id=user['user_id'], message=message):
            count += 1
    for admin in ADMIN_LIST:
        await bot.send_message(admin, text=f'Sent {count} of {len(users_data)} messages.')
