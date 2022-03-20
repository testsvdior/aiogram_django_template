import logging
from typing import Dict, Union, List
from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import exceptions

from handlers.services import get_detail_info, send_message, send_users
from loader import dp, bot
from requests import get_users_query, block_user_query
from settings import ADMIN_LIST
from handlers.exceptions import CommandArgumentError, NotFound
from keyboards.inline import get_exit_keyboard, get_user_detail_keyboard


@dp.message_handler(commands='users', user_id=ADMIN_LIST)
async def cmd_users(message: types.Message, state: FSMContext):
    """
    This handler will be called when user sends `/users`
    :param message: Telegram message with "/users" command.
    :param state: state that we create to user.
    """
    await send_users(message, state=state, payload={'page_size': 10, 'p': 1})


@dp.callback_query_handler(lambda c: c.data.startswith('page'), state='paginate')
async def clb_users_paginate(call: types.CallbackQuery, state: FSMContext):
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
async def clb_exit_from_state(call: types.CallbackQuery, state: FSMContext):
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
async def cmd_user_detail(message: types.Message, state: FSMContext):
    """
    Handler return user detail info.
    Example:
        "/detail 111222333" - will return info about user with ID 11122333
        "/111222333" will work when admin click on the state paginate

    :param message: message with command from Telegram.
    :param state: FSMContext - we need write here user_id of current user.
    """
    try:
        if message.text[1:].isdigit():
            user_id = message.text[1:]
        else:
            user_id: str = message.get_args()
        answer, is_banned = await get_detail_info(user_id=user_id)
        await message.answer(answer, reply_markup=await get_user_detail_keyboard(is_banned))
        await state.set_data({'users_data': [{'user_id': user_id, 'is_banned': is_banned}]})
    except exceptions.MessageTextIsEmpty:
        await message.answer("You didn't send user id!")
    except CommandArgumentError:
        await message.answer('ID must contains only digits.')
    except NotFound:
        await message.answer('User was not found.')


@dp.callback_query_handler(lambda c: c.data == 'message', state='*')
@dp.message_handler(commands='message', user_id=ADMIN_LIST)
async def cmd_message(action: Union[types.Message, types.CallbackQuery], state: FSMContext) -> None:
    answer = [
        'Send me message, that you want to send users.',
        'To cancel click the button below',
    ]
    # checking action is callback or message
    if isinstance(action, types.CallbackQuery):
        await action.message.delete_reply_markup()
        await action.message.answer('\n'.join(answer), reply_markup=await get_exit_keyboard())
    else:
        await action.answer('\n'.join(answer), reply_markup=await get_exit_keyboard())
    await state.set_state('message')


@dp.callback_query_handler(lambda c: c.data == 'block', state='paginate')
async def clb_block(call: types.CallbackQuery, state: FSMContext):
    """
    Handler using for block or unlock user.
    """
    state_data: Dict = await state.get_data()
    user_id: int = state_data.get('users_data')[0]['user_id']
    is_banned: bool = state_data.get('users_data')[0]['is_banned']
    if await block_user_query(user_id, is_banned):
        await call.message.edit_text(call.message.text, reply_markup=await get_user_detail_keyboard(not is_banned))
        await call.answer()
        await state.update_data({'users_data': [{'user_id': user_id, 'is_banned': not is_banned}]})
    else:
        await call.message.answer('An error has occurred')
        await state.finish()


@dp.message_handler(state='message')
async def msg_state_message(message: types.Message, state: FSMContext):
    await message.answer('Starting to send messages.')
    if await state.get_data('users_data'):
        state_data: Dict = await state.get_data()
        users_data: List[Dict[str, int]] = state_data.get('users_data')
        await state.set_state('paginate')
    else:
        users_data: List[Dict[str, int]] = await get_users_query(payload={'only_id': 1})
        await state.finish()
    count = 0
    for user in users_data:
        if await send_message(user_id=user['user_id'], message=message):
            count += 1
    for admin in ADMIN_LIST:
        try:
            notify_admin_text = f'Sent {count} of {len(users_data)} messages.'
            await bot.send_message(admin, text=notify_admin_text, reply_markup=await get_exit_keyboard())
        except exceptions.ChatNotFound as _:
            logging.error(f'Chat {admin} not found.')
