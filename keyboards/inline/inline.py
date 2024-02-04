from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Dict, List


async def kb_inline_league(btns_data: List[Dict], btns_pref: str) -> InlineKeyboardMarkup:
    inline_keyboard_markup = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    inline_keyboard_markup.add(*(InlineKeyboardButton(
        text=text['league_name'],
        callback_data=f'{btns_pref}_'
                      f'{text["league_name"]}_'
                      f'{text["league_id"]}_'
                      f'{text["country_name"]}_'
                      f'{text["country_id"]}_'
                      f'{text["league_type"]}_'
                      f'{text["league_sub_type"]}'
    )
        for text in btns_data
    )
                               )

    return inline_keyboard_markup


async def kb_inline_head_to_head(btns_data: List[Dict]) -> InlineKeyboardMarkup:
    inline_keyboard_markup = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    inline_keyboard_markup.add(*(InlineKeyboardButton(text=text['league_name']) for text in btns_data))

    return inline_keyboard_markup