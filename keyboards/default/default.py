from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from typing import Dict, List


async def kb_sth(btns_text: List[Dict]) -> ReplyKeyboardMarkup:
    keyboard_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    keyboard_markup.add(*(KeyboardButton(text=text['league_name']) for text in btns_text))

    return keyboard_markup


async def kb_seasons(btns_text: Dict) -> ReplyKeyboardMarkup:
    keyboard_markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=False)
    keyboard_markup.add(*(KeyboardButton(text=text['season_name']) for text in btns_text.values())) # row(KeyboardButton(text="All"))
    return keyboard_markup


async def kb_teams(btns_text: List) -> ReplyKeyboardMarkup:
    keyboard_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    keyboard_markup.add(*(KeyboardButton(text=text) for text in btns_text))
    return keyboard_markup


async def kb_livescore(btns_text: List[Dict]) -> ReplyKeyboardMarkup:
    keyboard_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    keyboard_markup.add(*(KeyboardButton(text=text['league_name']) for text in btns_text)) #  .row((KeyboardButton(text='All')))

    return keyboard_markup


async def kb_upcoming(btns_text: List[Dict]) -> ReplyKeyboardMarkup:
    keyboard_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    keyboard_markup.add(*(KeyboardButton(text=text['league_name']) for text in btns_text))  #  .row((KeyboardButton(text='All')))

    return keyboard_markup


async def kb_get_table(btns_text: List[Dict]) -> ReplyKeyboardMarkup:
    keyboard_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    keyboard_markup.add(*(KeyboardButton(text=text['league_name']) for text in btns_text if text['league_sub_type'] == 'domestic'))

    return keyboard_markup


async def kb_location() -> ReplyKeyboardMarkup:
    keyboard_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    keyboard_markup.add(KeyboardButton(text='Share your location', request_location=True)).add(KeyboardButton(text='Reject to share your location', request_location=False))

    return keyboard_markup