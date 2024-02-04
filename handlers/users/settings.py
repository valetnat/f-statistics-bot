from aiogram import types
from aiogram.dispatcher.filters import Text
import logging
import timezonefinder

from loader import bot, dp
from database.CRUD import update_user_timezone, add_query
from keyboards.default.default import kb_location


@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message) -> None:

    tz = timezonefinder.TimezoneFinder()
    tz_str: str = tz.certain_timezone_at(lat=message.location.latitude, lng=message.location.longitude)

    await update_user_timezone(data=message, user_timezone=tz_str)

    await message.reply(text=f"👍Your timezone adjusted successfully\nCurrent timezone - <b>{tz_str}</b>",
                        reply_markup=types.ReplyKeyboardRemove(),
                        parse_mode=types.ParseMode.HTML
                        )

    logging.info(f"Id: {message.from_user.id} - Settings command completed successfully")


@dp.message_handler(Text(startswith='Reject'))
async def handle_rejection(message: types.Message) -> None:

    await message.reply(text="🚫️Timezone has not been updated.",
                        reply_markup=types.ReplyKeyboardRemove(),
                        parse_mode=types.ParseMode.HTML
                        )


@dp.message_handler(commands=["settings"])
async def command_settings(message: types.Message) -> None:

    kb: types.ReplyKeyboardMarkup = await kb_location()

    await bot.send_message(message.from_user.id,
                           text="Please send your current location to adjust the timezone",
                           reply_markup=kb,
                           parse_mode=types.ParseMode.HTML
                           )

    await add_query(user_id=message.from_user.id, query_type=command_settings.__name__)
