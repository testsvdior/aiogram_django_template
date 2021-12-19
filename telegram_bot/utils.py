from typing import Dict, List


async def prepare_user_data(data: dict) -> Dict[str, str]:
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


async def prepare_users_list(data: list) -> List:
    users = []
    users.extend(
        [f'👤<a href="tg://user?id={i["user_id"]}">{i["first_name"]} {i.get("last_name", " ")}</a>' for i in data]
    )
    return users
