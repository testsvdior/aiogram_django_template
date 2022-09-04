import logging
from typing import Dict, Union, List

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.services import send_message
from loader import dp, bot_config
from requests import User
from keyboards.inline import get_exit_keyboard


@dp.callback_query_handler(lambda c: c.data == 'message', state='*')
@dp.message_handler(commands='message', user_id=bot_config.admin_list)
async def cmd_message(action: Union[types.Message, types.CallbackQuery], state: FSMContext) -> None:
    """
    Function used to send message to users.
    """
    logging.info(f'User [ID:{action.from_user.id}]: /message command')
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


@dp.message_handler(state='message')
async def msg_state_message(message: types.Message, state: FSMContext):
    logging.info('msg_state_message')
    await message.answer('Starting to send messages.')
    if await state.get_data('users_data'):
        state_data: Dict = await state.get_data()
        users_data: List[Dict[str, int]] = state_data.get('users_data')
        await state.set_state('paginate')
    else:
        users_data: List[Dict[str, int]] = await User.get_users_query(payload={'only_id': 1})
        await state.finish()
    count = 0
    if not users_data:
        await message.answer('No users found.')
        await state.set_state()
        return

    for user in users_data:
        if await send_message(user_id=user['user_id'], message=message):
            count += 1
    # notify admins about successfully sent messages
    for admin in bot_config.admin_list:
        await send_message(user_id=admin, message=f'Sent {count} of {len(users_data)} messages.')
