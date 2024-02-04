from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from typing import Optional, List, Dict
import logging

from loader import dp, bot

from site_api.all import get_standings, get_current_season_id
from states.users import GetTable
from database.CRUD import db_available_leagues, add_query
from keyboards.default.default import kb_get_table


@dp.message_handler(commands=["get_table"], state=None)
async def command_get_table(message: types.Message) -> None:

    await GetTable.league_name.set()

    result: Optional[List[dict]] = db_available_leagues()

    inline_kb: types.ReplyKeyboardMarkup = await kb_get_table(btns_text=result)

    await bot.send_message(chat_id=message.from_user.id,
                           text="<b>Choose league below: </b>",
                           reply_markup=inline_kb,
                           parse_mode='html'
                           )

    await add_query(user_id=message.from_user.id, query_type=command_get_table.__name__)


@dp.message_handler(state=GetTable.league_name)
async def process_league_choice(message: types.Message, state=FSMContext) -> None:

    async with state.proxy() as data:
        data['league_name'] = message.text

    result: Optional[List[Dict]] = db_available_leagues()

    available_league: List[int] = [elem["league_id"] for elem in result if elem['league_name'] == data['league_name']]

    cur_season_id: Optional[int] = await get_current_season_id(league_id=available_league[0])

    result: Optional[Dict[dict]] = await get_standings(league_id=available_league[0], current_season_id=cur_season_id)

    if result:
        sorted_by_position: Dict[dict] = dict(sorted(result.items(), key=lambda x: x))

        data: List[List[int, str]] = [
            [row, value["team_name"],
             value["games_played"],
             value["games_won"],
             value["games_lost"],
             value["games_draw"],
             value["points"]
             ]
            for row, value in sorted_by_position.items()
        ]

        max_columns: List[int] = []

        for col in zip(*data):
            len_el: List[int] = []
            [len_el.append(len(str(el))) for el in col]
            max_columns.append(max(len_el))

        columns: List[str] = ["", "", "Pl", "W", "D", "L", "Pts"]

        text_final: str = f'<code>{columns[0]:{max_columns[0] + 1}}' \
                          f'{columns[1]:{max_columns[1] + 1}}' \
                          f'{columns[2]:{max_columns[2] + 1}}' \
                          f'{columns[3]:{max_columns[3] + 1}}' \
                          f'{columns[4]:{max_columns[4] + 1}}' \
                          f'{columns[5]:{max_columns[5] + 1}}' \
                          f'{columns[6]:{max_columns[6] + 1}}</code>\n'

        for row, el in enumerate(data):

            text_final += f'<code>{el[0]:<{max_columns[0] + 1}}' \
                          f'{el[1]:<{max_columns[1]}}' \
                          f'{el[2]:{max_columns[2] + 1}}' \
                          f'{el[3]:{max_columns[3] + 1}}' \
                          f'{el[4]:{max_columns[4] + 1}}' \
                          f'{el[5]:{max_columns[5] + 1}}' \
                          f'{el[6]:{max_columns[6] + 1}}</code>\n'

        await bot.send_message(message.from_user.id,
                               text=text_final,
                               reply_markup=types.ReplyKeyboardRemove(),
                               parse_mode=types.ParseMode.HTML
                               )

        await state.finish()

        logging.info(f"Id: {message.from_user.id} - Get table command completed successfully")
