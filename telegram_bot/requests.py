import aiohttp

from utils import prepare_user_data
from settings import BACKEND_URL


async def create_user_query(data: dict):
    data = await prepare_user_data(data=data)
    async with aiohttp.ClientSession() as session:
        async with session.post(BACKEND_URL + 'api/user',
                                data=data) as response:
            # todo - запись логов в файл
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print("Body:", html, "...")
