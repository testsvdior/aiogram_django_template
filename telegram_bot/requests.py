from typing import List

import aiohttp

from settings import (
    BACKEND_URL,
    REQUEST_USER_LOGIN,
    REQUEST_USER_PASSWORD,
)

REFRESH_TOKEN: str = ''
ACCESS_TOKEN: str = ''


async def get_jwt_credentials() -> None:
    """
    Запрос запрашивает ключ для аутентификации.
    :return: ключ аутентификации.
    """
    url = BACKEND_URL + 'api/token/'
    data = {'username': REQUEST_USER_LOGIN, 'password': REQUEST_USER_PASSWORD}
    async with aiohttp.ClientSession() as session:
        async with session.post(
                url,
                data=data,
        ) as response:
            credentials = await response.json()
            global REFRESH_TOKEN, ACCESS_TOKEN
            REFRESH_TOKEN, ACCESS_TOKEN = (value for value in credentials.values())


async def create_user_query(data: dict) -> int:
    """
    Запрос на создание нового пользователя.
    :param data: user data
    :return: response status code
    """
    headers = {
        'Authorization': 'Bearer ' + ACCESS_TOKEN
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
                BACKEND_URL + 'api/user/',
                data=data,
                headers=headers,
        ) as response:
            print(await response.json())
            return response.status


async def get_users_list() -> List:
    headers = {
        'Authorization': 'Bearer ' + ACCESS_TOKEN
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(
                BACKEND_URL + 'api/users/',
                headers=headers,
        ) as response:

            response_data = await response.json()
            return response_data
