import logging
from typing import Dict

import aiohttp

from settings import BackendSettings


class AuthBackend:
    def __init__(self):
        self._credentials: Dict[str, str] = {
            'username': BackendSettings.username,
            'password': BackendSettings.password,
        }
        self._refresh_token: str = ''
        self._access_token: str = ''
        self._token_url = BackendSettings.url + 'api/token/'
        self._refresh_token_url = BackendSettings.url + 'api/token/refresh/'

    async def auth_user(self) -> None:
        """Method get and set auth token."""
        async with aiohttp.ClientSession() as session:
            async with session.post(self._token_url, data=self._credentials) as response:
                assert response.status, 200
                credentials = await response.json()
                self._refresh_token, self._access_token = (value for value in credentials.values())

    async def refresh_token(self) -> None:
        """Method refresh access token."""
        data = {"refresh": self._refresh_token}
        async with aiohttp.ClientSession() as session:
            async with session.post(self._refresh_token_url, data=data) as response:
                credentials = await response.json()
                if not credentials.get('access', None):
                    logging.info('Refresh token is expired')
                    await self.auth_user()
                    return

                self._access_token = credentials['access']

    async def get_auth_header(self) -> Dict[str, str]:
        """
        Method return header with authorization credentials.
        :return: header with auth credentials.
        """
        return {'Authorization': 'Bearer ' + self._access_token}
