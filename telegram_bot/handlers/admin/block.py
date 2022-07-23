import logging
from typing import Dict

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from requests import User
from keyboards.inline import get_user_detail_keyboard


@dp.callback_query_handler(lambda c: c.data == 'block', state='paginate')
async def clb_block(call: types.CallbackQuery, state: FSMContext):
    """
    Handler using for block or unlock user.
    """
    logging.info('clb_block')
    state_data: Dict = await state.get_data()
    user_id: int = state_data.get('users_data')[0]['user_id']
    is_banned: bool = state_data.get('users_data')[0]['is_banned']
    if await User.block_user_query(user_id, is_banned):
        await call.message.edit_text(call.message.text, reply_markup=await get_user_detail_keyboard(not is_banned))
        await call.answer()
        await state.update_data({'users_data': [{'user_id': user_id, 'is_banned': not is_banned}]})
        logging.info(
            f'User {call.from_user.id} {"blocked" if not is_banned else "unblocked"} user with ID {user_id}')
    else:
        await call.message.answer('An error has occurred')
        await state.finish()
