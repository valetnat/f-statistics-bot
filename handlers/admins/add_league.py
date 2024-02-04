from aiogram import types
from aiogram.dispatcher.filters import Text
from typing import Optional, Dict, List

import logging

from loader import dp, bot
from keyboards.inline.inline import kb_inline_league
from site_api.all import get_all_leagues, get_teams, api_get_teams_example
from site_api.match_scores import api_get_teams

from database.CRUD import db_available_leagues, db_add_league, add_query, db_create_league_table, db_add_teams


@dp.message_handler(commands=["add_league"], is_admin=True)
async def command_add_league(message: types.Message) -> None:

    result: Optional[List[dict]] = db_available_leagues()
    leagues: Optional[List[dict]] = await get_all_leagues()

    inline_kb: types.InlineKeyboardMarkup = await kb_inline_league(btns_data=leagues, btns_pref='add')

    text_result = f"<b>🗄Available league(s) of database:</b>\n\n".upper()

    if result:

        for elem in result:
            text_result += f"🟢 {elem['league_name']}\n"

        await bot.send_message(chat_id=message.from_user.id,
                               text=text_result + "\n<b>Choose a league to add below: </b>",
                               reply_markup=inline_kb,
                               parse_mode=types.ParseMode.HTML
                               )
    else:
        text_result += f"🔴️ None\n\n<b>Choose a league to add below: </b>"

        await bot.send_message(chat_id=message.from_user.id,
                               text=text_result,
                               reply_markup=inline_kb,
                               parse_mode=types.ParseMode.HTML
                               )

    await add_query(user_id=message.from_user.id,
                    query_type=command_add_league.__name__
                    )


@dp.callback_query_handler(Text(startswith="add_"))
async def callback_add_league(callback: types.CallbackQuery) -> None:

    result: bool = await db_add_league(data=callback.data.split("_"),
                                       user_id=callback.from_user.id
                                       )

    if result:
        await callback.answer(text=f"👍{callback.data.split('_')[1]} added to database successfully",
                              show_alert=True
                              )

        await db_create_league_table(name=callback.data.split('_')[1])

        result: Optional[Dict] = await api_get_teams_example(country_id=callback.data.split('_')[4])

        await db_add_teams(table_name=callback.data.split('_')[1],
                           data=result
                           )

        logging.info(f'Id: {callback.from_user.id} - Add_league command completed successfully')

    else:
        await callback.answer(text=f"‼️This league exists in database. Choose another league",
                              show_alert=True
                              )