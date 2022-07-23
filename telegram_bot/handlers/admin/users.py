import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.services import send_users
from loader import dp
from settings import ADMIN_LIST


@dp.message_handler(commands='users', user_id=ADMIN_LIST)
async def cmd_users(message: types.Message, state: FSMContext):
    """
    This handler will be called when user sends `/users`
    :param message: Telegram message with "/users" command.
    :param state: state that we create to user.
    """
    logging.info(f'User with ID {message.from_user.id} called /users command')
    await send_users(message, state=state, payload={'page_size': 10, 'p': 1})


@dp.callback_query_handler(lambda c: c.data.startswith('page'), state='paginate')
async def clb_users_paginate(call: types.CallbackQuery, state: FSMContext):
    """
    This handler will be called when user touch inline keyboards from message with paginate.
    :param call: Telegram callback query with data that startswith "page".
    :param state: state that we create to user.
    """
    logging.info('clb_users_paginate')
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
    logging.info('clb_exit_from_state')
    await state.finish()
    await call.message.delete_reply_markup()
    await call.message.delete()
