from aiogram.types import BotCommandScopeDefault, BotCommand, BotCommandScopeChat

import logging

from loader import bot


def get_default_commands() -> list[BotCommand]:
    commands: list[BotCommand] = [
        BotCommand(command='/start', description='start the bot'),
        BotCommand(command='/help', description='how to use'),
        BotCommand(command='/head_to_head', description='get the football match scores between chosen teams'),
        BotCommand(command='/livescore', description='get livescores'),
        BotCommand(command='/upcoming', description='get information about upcoming matches'),
        BotCommand(command='/get_table', description='get a league table'),
        BotCommand(command='/settings', description='set your timezone to display valid time')
    ]

    return commands


async def set_default_commands() -> None:
    await bot.set_my_commands(get_default_commands(), scope=BotCommandScopeDefault())
    logging.info(f'Default commands added')


async def set_user_commands(chat_id: int) -> None:
    await bot.set_my_commands(get_default_commands(), scope=BotCommandScopeChat(chat_id))
    logging.info(f'User commands added')