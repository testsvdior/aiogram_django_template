from typing import Dict, Union, List

import aiohttp

from settings import BACKEND_URL
from loader import auth


async def create_user_query(data: dict) -> int:
    """
    Function created new Telegram user to Backend.
    :param data: user data
    :return: response status code
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(
                BACKEND_URL + 'api/user/',
                data=data,
                headers=await auth.get_auth_header(),
        ) as response:
            return response.status


async def get_users_data(payload: Dict = None) -> Union[Dict, List[Dict]]:
    """
    Function return telegram users list from backend.
    :param payload: request params.
    :return: dict with data about users.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
                BACKEND_URL + 'api/users/',
                headers=await auth.get_auth_header(),
                params=payload,
        ) as response:
            response_data = await response.json()
            return response_data


async def get_user_detail(user_id: str):
    """
    GET query to endpoint that return user detail.
    :param user_id: Telegram user ID.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
                BACKEND_URL + f'api/user/{user_id}',
                headers=await auth.get_auth_header(),
        ) as response:
            response_data = await response.json()
            return response_data
