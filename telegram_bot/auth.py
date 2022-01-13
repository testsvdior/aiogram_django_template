from typing import Dict

import aiohttp

from settings import REQUEST_USER_LOGIN, REQUEST_USER_PASSWORD, BACKEND_URL


class AuthBackend:
    def __init__(self):
        self._credentials: Dict[str, str] = {
            'username': REQUEST_USER_LOGIN,
            'password': REQUEST_USER_PASSWORD,
        }
        self._refresh_token: str = ''
        self._access_token: str = ''
        self._token_url = BACKEND_URL + 'api/token/'
        self._refresh_token_url = BACKEND_URL + 'api/token/refresh/'

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
                assert response.status, 200
                credentials = await response.json()
                self._access_token = credentials['access']

    async def get_auth_header(self) -> Dict[str, str]:
        """
        Method return header with authorization credentials.
        :return: header with auth credentials.
        """
        return {'Authorization': 'Bearer ' + self._access_token}
