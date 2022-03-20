import logging
from typing import Dict, Union, List

import aiohttp

from handlers.exceptions import NotFound
from settings import BACKEND_URL
from loader import auth


async def create_user_query(data: Dict) -> int:
    """
    Function created new Telegram user to Backend.
    :param data: user data.
    :return: response status code.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(
                BACKEND_URL + 'api/users/',
                data=data,
                headers=await auth.get_auth_header(),
        ) as response:
            return response.status


async def get_users_query(payload: Dict = None) -> Union[Dict, List[Dict]]:
    """
    Function return telegram users list from backend.
    :param payload: request params.
    :return: Dict with data about users or List with user_id of users.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
                BACKEND_URL + 'api/users/',
                headers=await auth.get_auth_header(),
                params=payload,
        ) as response:
            response_data = await response.json()
            return response_data


async def get_user_detail_query(user_id: str) -> Dict:
    """
    GET query to endpoint that return user detail.
    :param user_id: Telegram user ID.
    :return: Dict with data about user.

    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
                BACKEND_URL + f'api/users/{user_id}',
                headers=await auth.get_auth_header(),
        ) as response:
            response_data = await response.json()
            if response.status == 404:
                raise NotFound
            return response_data


async def block_user_query(user_id: int) -> bool:
    """
    PUT query to endpoint that block user.
    :param user_id: Telegram user ID.
    """
    data = {'is_banned': 1}
    async with aiohttp.ClientSession() as session:
        async with session.patch(
                BACKEND_URL + f'api/users/{user_id}',
                headers=await auth.get_auth_header(),
                data=data,
        ) as response:
            logging.info(f'Block query response status == {response.status}')
            return True if response.status == 200 else False
