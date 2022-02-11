from handlers.exceptions import CommandArgumentError
from requests import get_user_detail
from utils import prepare_user_detail


async def get_detail_info(user_id: str):
    """Function return user detail data."""
    if not user_id.isdigit():
        raise CommandArgumentError
    result = await get_user_detail(user_id=user_id)
    answer = await prepare_user_detail(result)
    return answer
