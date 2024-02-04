import logging

from aiogram.types import BotCommand, BotCommandScopeChat

from loader import bot
from utils.set_default_commands import get_default_commands


def get_admin_commands() -> list[BotCommand]:
    commands = get_default_commands()

    commands.extend([
        BotCommand('/add_league', 'add league to the available leagues'),
        BotCommand('/del_league', 'delete league from the available leagues')
    ])

    return commands


async def set_admin_commands(chat_id: int) -> None:
    await bot.set_my_commands(get_admin_commands(), scope=BotCommandScopeChat(chat_id))
    logging.info(f'Admin commands added')