from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from typing import Optional, List, Dict
import logging

from loader import dp, bot
from site_api.all import get_upcoming_event
from states.users import UpComing
from database.CRUD import db_available_leagues, add_query
from keyboards.default.default import kb_upcoming
from utils.utc_to_local import utc_to_local


@dp.message_handler(commands=["upcoming"], state=None)
async def command_upcoming(message: types.Message) -> None:

    await UpComing.league_name.set()

    result: Optional[List[dict]] = db_available_leagues()

    inline_kb: types.ReplyKeyboardMarkup = await kb_upcoming(btns_text=result)

    await bot.send_message(
        chat_id=message.from_user.id,
        text="<b>Choose league below:</b>",
        reply_markup=inline_kb,
        parse_mode='html'
    )

    await add_query(user_id=message.from_user.id, query_type=command_upcoming.__name__)

@dp.message_handler(state=UpComing.league_name)
async def process_league_choice(message: types.Message, state=FSMContext) -> None:
    async with state.proxy() as data:
        data['league_name'] = message.text

    result: Optional[List[dict]] = db_available_leagues()

    available_league: List[str] = [elem["league_name"] for elem in result]

    result: Dict[List[dict]] = await get_upcoming_event()

    if result:

        for league in result.keys():
            final_text: str = f"<b>Upcoming match(es) for {league}:</b>\n\n".upper()
            if (league == data['league_name']) and (league in available_league):
                for match in result[league]:
                    date_local = await utc_to_local(match_date=match['starting_at'], message=message)
                    final_text += f"<b>🗓 {date_local.strftime('%b %d %Y  %H:%M')}</b>:\n      {match['match_name']}\n\n"
                final_text += f'<a href="t.me/FstaticticBot/"><u>t.me/FstaticticBot/</u></a>'
                await bot.send_message(message.from_user.id,
                                       text=final_text,
                                       reply_markup=types.ReplyKeyboardRemove(),
                                       parse_mode=types.ParseMode.HTML
                                       )
                break
        else:
            await message.reply(text=f"‼️There are no upcoming matches for {data['league_name']}",
                                reply_markup=types.ReplyKeyboardRemove(),
                                parse_mode=types.ParseMode.HTML
                                )
    else:
        await message.reply(text=f"‼️Upcoming matches were not found",
                            reply_markup=types.ReplyKeyboardRemove(),
                            parse_mode=types.ParseMode.HTML
                            )

    await state.finish()

    logging.info(f"Id: {message.from_user.id} - Upcoming command completed successfully")