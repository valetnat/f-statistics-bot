# from aiogram import types, Dispatcher
# from aiogram.dispatcher import FSMContext
# import datetime
# import logging
#
# from data.config import AVAILABLE_LEAGUES, ADMINS
# from utils import set_user_commands, set_admin_commands
# from loader import bot
# from states.users import Form
#
# # from keyboards.user_kb import b_1, b_2, b_3, b_4
#
#
# async def get_statistic(message: types.Message):
#     # Set state
#     await Form.league_name.set()
#
#     await message.reply("What a league you are interested in?")
#     await message.answer(f"{list(AVAILABLE_LEAGUES.values())}")
#
#
# async def process_league_name(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['league_name'] = message.text
#
#     await Form.next()
#
#     await message.reply("Choose season you want")
#     await message.answer("2023, 2022, 2021, 2021, ALl Season")
#
#
# async def process_season(message: types.Message, state: FSMContext):
#
#     await Form.next()
#     await state.update_data(season=message.text)
#
#     await message.reply(text="Choose first team from: ")
#     await message.answer(text="Liverpool, AC Milan, Barcelona, Inter")
#
#
# async def process_team_1(message: types.Message, state: FSMContext):
#
#     await Form.next()
#     await state.update_data(team_1=message.text)
#
#     await message.reply(text="Choose second team from:")
#     await message.answer(text="Liverpool, Barcelona, Inter")
#
#
# async def process_team_2(message: types.Message, state: FSMContext):
#
#     async with state.proxy() as data:
#         data['team_2'] = message.text
#
#     await bot.send_message(message.from_user.id, text=f"League: {data['league_name']}\n"
#                                                       f"Season: {data['season']}\n"
#                                                       f"Teams: {data['team_1']} vs {data['team_2']}")
#     await state.finish()
#
#
# from loader import cursor
#
#
#
#
#
#
#
# # async def command_start(message: types.Message):
# #
# #     query: str = "SELECT `tg_user_id` FROM `user`;"
# #     cursor.execute(query)
# #     for user_tpl in cursor:
# #         await bot.send_message(message.from_user.id, text=user_tpl)
# #     else:
# #         await bot.send_message(message.from_user.id, text="NONE user")
# #
# #
# #     await set_admin_commands(message.chat.id) if str(message.from_user.id) in ADMINS else await set_user_commands(message.chat.id)
# #
# #     await bot.send_message(message.from_user.id, text=f"Welcome to FstaticBot")
# #     logging.info(f"Id: {message.from_user.id} -  Start command completed successfully")
# #
# #
# # async def command_help(message: types.Message):
# #     commands = await bot.get_my_commands(scope=types.BotCommandScopeChat(chat_id=message.chat.id))
# #
# #     text = ("Here you can get comprehensive statistic from chosen football teams and its games!\n"
# #             "\nThe following commands are available:\n\n")
# #     for command in commands:
# #         text += f"/{command.command} - {command.description}\n"
# #
# #     await bot.send_message(message.from_user.id, text=text)
# #     logging.info(f"Id: {message.from_user.id} - Help command completed successfully")
#
#
# async def get_text(message: types.Message):
#     await message.answer(f"Got your message")
#     logging.info(f"Id: {message.from_user.id} - Text command completed successfully")
#
#
# async def get_league(message: types.Message):
#     leagues = []
#     query = "SELECT * FROM `leagues`;"
#     cursor.execute(query)
#
#     await bot.send_message(message.from_user.id, text=[league[1] for league in cursor])
#     # for key, value in AVAILABLE_LEAGUES.items():
#     #     await message.answer(f"{key}: {value}")
#     logging.info(f"Id: {message.from_user.id} - Text command completed successfully")
#
#
# def register_handlers_commands(dp: Dispatcher):
#     # dp.register_message_handler(command_start, commands="start")
#     # dp.register_message_handler(command_help, commands="help")
#     dp.register_message_handler(get_league, commands="get_league")
#     dp.register_message_handler(get_statistic, commands="get_statistic")
#
#     dp.register_message_handler(process_league_name, state=Form.league_name)
#     dp.register_message_handler(process_season, state=Form.season)
#     dp.register_message_handler(process_team_1, state=Form.team_1)
#     dp.register_message_handler(process_team_2, state=Form.team_2)
#
#     logging.info("User commands registered successfully")
