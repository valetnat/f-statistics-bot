from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from typing import Optional, Dict, List
import logging

from loader import dp, bot
from site_api.all import get_livescore
from states.users import LiveScore
from database.CRUD import db_available_leagues, add_query
from keyboards.default.default import kb_livescore


@dp.message_handler(commands=["livescore"], state=None)
async def command_livescore(message: types.Message) -> None:

    await LiveScore.league_name.set()

    result: Optional[List[dict]] = db_available_leagues()

    inline_kb: types.ReplyKeyboardMarkup = await kb_livescore(btns_text=result)

    await bot.send_message(chat_id=message.from_user.id,
                           text="<b>Choose league below:</b>",
                           reply_markup=inline_kb,
                           parse_mode=types.ParseMode.HTML
                           )

    await add_query(user_id=message.from_user.id, query_type=command_livescore.__name__)


@dp.message_handler(state=LiveScore.league_name)
async def process_league_choice(message: types.Message, state=FSMContext) -> None:
    async with state.proxy() as data:
        data['league_name'] = message.text

    result: Optional[Dict] = await get_livescore()

    if result:

        final_text: str = f"<b>Livescore for {data['league_name']}:</b>\n\n".upper()

        if data['league_name'] in [league["league_name"] for league in result.values()]:

            for match, value in result.items():
                if value["league_name"] == data['league_name']:
                    if value['cur_minute']:
                        final_text += f"🔴 {value['cur_period']}: {value['cur_minute']}min\n      {value['home_team_name']} {value['score_home']}:{value['score_away']} {value['away_team_name']}\n\n"
                    else:
                        final_text += f"🔴 {value['cur_period']}:\n      {value['home_team_name']} {value['score_home']}:{value['score_away']} {value['away_team_name']}\n\n"

            await bot.send_message(chat_id=message.from_user.id,
                                   text=final_text,
                                   reply_markup=types.ReplyKeyboardRemove(),
                                   parse_mode=types.ParseMode.HTML
                                   )
        else:
            await message.reply(text=f"‼️Inplay matches were not found",
                                reply_markup=types.ReplyKeyboardRemove(),
                                parse_mode=types.ParseMode.HTML
                                )

    else:
        await message.reply(text=f"‼️Inplay matches were not found",
                            reply_markup=types.ReplyKeyboardRemove(),
                            parse_mode=types.ParseMode.HTML
                            )

    await state.finish()

    logging.info(f"Id: {message.from_user.id} - Livescore command completed successfully")