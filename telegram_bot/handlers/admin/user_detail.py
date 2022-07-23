import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import exceptions

from handlers.services import get_detail_info
from loader import dp
from settings import ADMIN_LIST
from handlers.exceptions import CommandArgumentError, NotFound
from keyboards.inline import get_user_detail_keyboard


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
    logging.info(f'User [ID:{message.from_user.id}]: /detail command')
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
