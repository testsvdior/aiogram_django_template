from typing import List

import aiohttp

from settings import BACKEND_URL


async def create_user_query(data: dict) -> int:
    """
    Запрос на создание нового пользователя.
    :param data: user data
    :return: response status code
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(
                BACKEND_URL + 'api/user/',
                data=data,
        ) as response:
            return response.status


async def get_users_list() -> List:
    async with aiohttp.ClientSession() as session:
        async with session.get(
                BACKEND_URL + 'api/users/',
        ) as response:
            response_data = await response.json()
            return response_data
