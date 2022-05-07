import logging
from typing import Dict, Union, List

import aiohttp

from settings import BACKEND_URL
from loader import auth
from handlers.exceptions import NotFound


class User:
    """Class that work with /users/ endpoint."""
    prefix: str = 'api/users/'
    endpoint: str = BACKEND_URL + prefix

    @classmethod
    async def create_user_query(cls, data: Dict) -> int:
        """
        Method create new Telegram user in Backend.

        :param data: user data.
        :return: response status code.
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    cls.endpoint,
                    data=data,
                    headers=await auth.get_auth_header(),
            ) as response:
                logging.info(f'POST: create_user_query return status - {response.status}')
                return response.status

    @classmethod
    async def get_users_query(cls, payload: Dict = None) -> Union[Dict, List[Dict]]:
        """
        Method return telegram users list from backend.

        :param payload: request params.
        :return: Dict with data about users or List with user_id of users.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    cls.endpoint,
                    headers=await auth.get_auth_header(),
                    params=payload,
            ) as response:
                logging.info(f'GET: get_users_query return status - {response.status}')
                return await response.json()

    @classmethod
    async def get_user_detail_query(cls, user_id: str) -> Dict:
        """
        Method return concrete user data.

        :param user_id: Telegram user ID.
        :return: Dict with data about user.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    cls.endpoint + user_id,
                    headers=await auth.get_auth_header(),
            ) as response:
                logging.info(f'GET: get_user_detail_query return status - {response.status}')
                if response.status == 404:
                    raise NotFound
                return await response.json()

    @classmethod
    async def block_user_query(cls, user_id: int, is_banned: bool) -> bool:
        """
        Method using for block users.

        :param user_id: Telegram user ID.
        :param is_banned: user ban status.
        """
        is_banned = 1 if is_banned is False else 0
        data = {'is_banned': is_banned}
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                    cls.endpoint + str(user_id),
                    headers=await auth.get_auth_header(),
                    data=data,
            ) as response:
                logging.info(f'PATCH: block_user_query response status - {response.status}')
                return True if response.status == 200 else False
