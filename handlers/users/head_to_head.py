from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text
import logging
from typing import Optional, Dict, List

from loader import dp, bot
from site_api.match_scores import api_head_to_head, api_get_available_season, api_get_teams
from states.users import HeadToHead
from database.CRUD import db_available_leagues, db_get_teams, add_query
from keyboards.default.default import kb_sth, kb_seasons, kb_teams
from utils.utc_to_local import utc_to_local


@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state=FSMContext) -> None:
    current_state = state.get_state()

    if current_state is None:
        return

    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Command canceled"
                           )
    await state.finish()


@dp.message_handler(commands=["head_to_head"], state=None)
async def command_head_to_head(message: types.Message) -> None:

    await HeadToHead.league_name.set()

    result: Optional[List[dict]] = db_available_leagues()

    inline_kb: types.ReplyKeyboardMarkup = await kb_sth(btns_text=result)

    await bot.send_message(chat_id=message.from_user.id,
                           text="<b>Choose league below: </b>",
                           reply_markup=inline_kb,
                           parse_mode='html'
                           )

    await add_query(user_id=message.from_user.id, query_type=command_head_to_head.__name__)


@dp.message_handler(state=HeadToHead.league_name)
async def process_league_choice(message: types.Message, state=FSMContext) -> None:

    async with state.proxy() as data:
        data['league_name'] = message.text

    result: Optional[Dict] = await api_get_available_season(league_name=data['league_name'])

    sorted_by_season_name: Dict = dict(sorted(result.items(), key=lambda x: x[1]['season_name']))

    await HeadToHead.next()

    inline_kb: types.ReplyKeyboardMarkup = await kb_seasons(btns_text=sorted_by_season_name)

    await bot.send_message(chat_id=message.from_user.id,
                           text="<b>Choose a season below:</b>",
                           reply_markup=inline_kb,
                           parse_mode="html"
                           )


@dp.message_handler(state=HeadToHead.season)
async def process_season_choice(message: types.Message, state=FSMContext) -> None:

    async with state.proxy() as data:
        data['season'] = message.text

    result: Optional[List[dict]] = db_available_leagues()

    country_id: List[int] = [elem["country_id"]
                             for elem in result
                             if data['league_name'] == elem['league_name']
                             ]

    league_id: List[int] = [elem["league_id"]
                            for elem in result
                            if data['league_name'] == elem['league_name']
                            ]

    read: Optional[List] = await api_get_teams(country_id=country_id[0],
                                               season_name=data['season'],
                                               league_id=league_id[0]
                                               )

    await HeadToHead.next()

    inline_kb: types.ReplyKeyboardMarkup = await kb_teams(btns_text=read)

    await bot.send_message(chat_id=message.from_user.id,
                           text="<b>Choose 1st team below:</b>",
                           reply_markup=inline_kb,
                           parse_mode=types.ParseMode.HTML
                           )


@dp.message_handler(state=HeadToHead.team_1)
async def process_team1_choice(message: types.Message, state=FSMContext) -> None:

    async with state.proxy() as data:
        data['team_name_1'] = message.text

    await HeadToHead.next()

    await bot.send_message(chat_id=message.from_user.id,
                           text="<b>Choose 2nd team below:</b> ",
                           parse_mode=types.ParseMode.HTML
                           )


@dp.message_handler(state=HeadToHead.team_2)
async def process_team2_choice(message: types.Message, state=FSMContext):

    async with state.proxy() as data:
        if data['team_name_1'] == message.text:
            await message.reply(text="‼️Error: the entered teams are the same. Please try again!", reply_markup=types.ReplyKeyboardRemove())
            await state.finish()
        else:
            data['team_name_2'] = message.text

            await HeadToHead.next()

            await bot.send_message(chat_id=message.from_user.id,
                                   text="<b>Enter the max number of results to display, if any:</b>",
                                   reply_markup=types.ReplyKeyboardRemove(),
                                   parse_mode=types.ParseMode.HTML
                                   )


@dp.message_handler(state=HeadToHead.result_number)
async def process_result_choice(message: types.Message, state=FSMContext) -> None:

    async with state.proxy() as data:
        data['result_number'] = message.text

    async with state.proxy() as data:
        try:

            result: Optional[List[dict]] = db_available_leagues()

            league_id: List[int] = [elem["league_id"]
                                    for elem in result
                                    if data['league_name'] == elem['league_name']
                                    ]

            result_team: Optional[Dict] = await db_get_teams(table_name=data['league_name'],
                                                             team_name_1=data['team_name_1'],
                                                             team_name_2=data['team_name_2']
                                                             )

            result: Optional[Dict] = await api_head_to_head(team_id_1=result_team[data['team_name_1']],
                                                            team_id_2=result_team[data['team_name_2']],
                                                            league_id=league_id[0],
                                                            season_name=data['season']
                                                            )

            result: Dict = dict(sorted(result.items(), key=lambda x: x[1]['played_at'], reverse=True))

            if result:
                final_text = f"<b>All football matches in {data['season']} season of {data['league_name']}:</b>\n\n".upper()

                for match, value in result.items():
                    if match == int(data["result_number"]):
                        break
                    date_local = await utc_to_local(match_date=value['played_at'], message=message)

                    final_text += f"<b>🗓 {date_local.strftime('%b %d %Y  %H:%M')}:</b>\n      {value['home_team_name']} {value['score_home']}:{value['score_away']} {value['away_team_name']}\n\n"

                final_text += f'<a href="t.me/FstaticticBot/"><u>t.me/FstaticticBot/</u></a>'
                await bot.send_message(chat_id=message.from_user.id,
                                       text=final_text,
                                       parse_mode=types.ParseMode.HTML
                                       )

            else:
                await message.reply(text=f"‼️{data['team_name_1']} and {data['team_name_1']} have not competed so far",
                                    parse_mode=types.ParseMode.HTML
                                    )

            logging.info(f"Id: {message.from_user.id} - Head to head command completed successfully")

        except ValueError as exp:
            await message.reply(text="‼️Error: the result number must be the integer. Please try again!",
                                reply_markup=types.ReplyKeyboardMarkup()
                                )
        finally:
            await state.finish()

