from aiogram import types
from typing import Tuple
import logging

from data.config import ADMINS
from utils import set_user_commands, set_admin_commands
from loader import bot, dp
from database.CRUD import get_users, add_user, update_user, add_query


@dp.message_handler(commands=["start"])
async def command_start(message: types.Message) -> None:

    await bot.send_message(message.from_user.id,
                           text=f"📈 Welcome to FstatisticBot",
                           parse_mode=types.ParseMode.HTML
                           )

    result: Tuple[int] = await get_users()

    if message.from_user.id in result:
        await update_user(data=message, is_admin=1) \
            if str(message.from_user.id) in ADMINS \
            else await update_user(data=message, is_admin=0)

    else:
        add_user(data=message, is_admin=1) \
            if str(message.from_user.id) in ADMINS \
            else add_user(data=message, is_admin=0)

    await set_admin_commands(message.chat.id) \
        if str(message.from_user.id) in ADMINS \
        else await set_user_commands(message.chat.id)

    await add_query(user_id=message.from_user.id,
                    query_type=command_start.__name__
                    )

    logging.info(f"Id: {message.from_user.id} -  Start command completed successfully")


@dp.message_handler(commands=["help"])
async def command_help(message: types.Message) -> None:
    commands = await bot.get_my_commands(scope=types.BotCommandScopeChat(chat_id=message.chat.id))

    text: str = "‼️Here you can get comprehensive statistics from chosen football teams and its games!\n" \
                "\nThe following commands are available:\n\n"

    for command in commands:
        text += f"/{command.command} - {command.description}\n"

    await bot.send_message(message.from_user.id, text=text)

    await add_query(user_id=message.from_user.id, query_type=command_help.__name__)

    logging.info(f"Id: {message.from_user.id} - Help command completed successfully")