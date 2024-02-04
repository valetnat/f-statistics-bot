from typing import Union
from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

import logging

from data import config


class IsAdmin(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: bool) -> None:
        self.is_admin = is_admin

    async def check(self, message: Union[types.Message, types.CallbackQuery]) -> bool:
        logging.info(f"Filter <{IsAdmin.__name__}> runs")
        user = message.from_user

        if str(user.id) in config.ADMINS:
            logging.info(f"Message passed the Filter <{IsAdmin.__name__}>")

            return self.is_admin is True

        logging.info(f"Message failed the Filter <{IsAdmin.__name__}>")
        return self.is_admin is False