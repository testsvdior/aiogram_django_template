import logging
from typing import Dict, List, Tuple


async def prepare_user_data(data: Dict) -> Dict[str, str]:
    """
    Function prepares user data for sending to the server.
    Обработка данных пользователя для дальнейшей отправки на сервер Django и сохранения в БД.
    :param data: types.Message.to_python()
    """
    correct_dict = {
        'user_id': data.get('id'),
        'username': data.get('username', ''),
        'first_name': data.get('first_name'),
        'last_name': data.get('last_name', ''),
        'language_code': data.get('language_code'),
    }
    return correct_dict


async def prepare_users_list(data: List) -> List:
    """
    Фунцкия форматирует ответ со списком пользователей в HTML формат с линком на каждого пользователя.
    :param data: список пользователей.
    """
    users = ['<b>Users list:</b>\n']
    users.extend(
        [f'👤<a href="tg://user?id={u["user_id"]}">{u["first_name"]} {u.get("last_name", " ")}</a> /{u["user_id"]}'
         for u in data]
    )
    return users


async def prepare_user_detail(data: Dict) -> Tuple[str, bool]:
    """
    Function prepare user data for answer.
    :param data: User data.
    """
    answer = ['<b>User detail:</b>\n']
    is_banned = data.pop('is_banned')
    answer.extend([f'<b>{key}</b>: <code>{value}</code>' for key, value in data.items()])
    return '\n'.join(answer), is_banned
