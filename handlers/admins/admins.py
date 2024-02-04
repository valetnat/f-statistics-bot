# from aiogram import types, Dispatcher

# import logging
#
# from loader import cursor
# from keyboards.user_kb import kb_admins_leagues


# async def add_league(message: types.Message):
#     leagues = []
#     query = "SELECT * FROM `leagues`;"
#     cursor.execute(query)
#
#     kb_result = kb_admins_add_leagues([league[1] for league in cursor])
#
#     await message.reply(text="Choose league to add league:", reply_markup=kb_result)
#     logging.info(f'Id: {message.from_user.id} - Add_league command completed successfully')


# async def del_league(message: types.Message):
#     leagues = []
#     query = "SELECT * FROM `leagues`;"
#     cursor.execute(query)
#
#     kb_result = kb_admins_add_leagues([league[1] for league in cursor])
#     await message.reply(text="Choose league to delete below:", reply_markup=kb_result)
#
#     logging.info(f'Id: {message.from_user.id} - Del_league command completed successfully')


# async def example_command(message: types.Message):
#     await message.reply(text="Got message. Next step soon")
#     logging.info(f'Id: {message.from_user.id} - Example command completed successfully')


# def register_handlers_commands(dp: Dispatcher):
    # dp.register_message_handler(add_league, commands="add_league", is_admin=True)
    # dp.register_message_handler(del_league, commands="del_league", is_admin=True)
    # dp.register_message_handler(example_command, commands="example", is_admin=True)
    # logging.info('Admin commands registered successfully')