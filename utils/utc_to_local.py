from aiogram import types
from typing import List
from datetime import datetime
import pytz

from database.CRUD import get_user_timezone


async def utc_to_local(match_date: str, message: types.Message) -> datetime:

    result = await get_user_timezone(user_id=message.from_user.id)
    local_tz = pytz.timezone(result)
    # local_tz = "Etc/GMT-3"

    return datetime.strptime(match_date, '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.utc).astimezone(local_tz)