from aiogram import Dispatcher, types
import logging

from data.config import ADMINS


async def on_start_up_notify(dp: Dispatcher) -> None:
    for admin in ADMINS:
        try:
            await dp.bot.send_message(chat_id=admin,
                                      text="<b>🚀 Bot has been launched</b>",
                                      parse_mode=types.ParseMode.HTML
                                      )
        except Exception as exp:
            logging.exception(exp)


async def on_shutdown_notify(dp: Dispatcher) -> None:
    for admin in ADMINS:
        try:
            await dp.bot.send_message(chat_id=admin,
                                      text="<b>🚨 Bot has been stopped</b>",
                                      parse_mode=types.ParseMode.HTML
                                      )
        except Exception as exp:
            logging.exception(exp)