from aiogram import types
from aiogram.dispatcher.filters import Text
from typing import Optional, List
import logging

from loader import dp, bot
from keyboards.inline.inline import kb_inline_league
from database.CRUD import db_available_leagues, db_del_league, db_table_delete, add_query


@dp.message_handler(commands=["del_league"], is_admin=True)
async def command_del_league(message: types.Message) -> None:

    result: Optional[List[dict]] = db_available_leagues()
    inline_kb: types.InlineKeyboardMarkup = await kb_inline_league(btns_data=result, btns_pref='del')

    text_result = f"<b>🗄Available league(s) of database:</b>\n\n".upper()
    if result:

        for elem in result:
            text_result += f"🟢 {elem['league_name']}\n"

        await bot.send_message(chat_id=message.from_user.id,
                               text=text_result + "\n<b>Choose a league to delete below: </b>",
                               reply_markup=inline_kb,
                               parse_mode=types.ParseMode.HTML
                               )

        await add_query(user_id=message.from_user.id,
                        query_type=command_del_league.__name__
                        )
    else:
        await message.reply(text="‼️There are no leagues to delete...",
                            parse_mode=types.ParseMode.HTML
                            )


@dp.callback_query_handler(Text(startswith="del_"))
async def callback_del_league(callback: types.CallbackQuery) -> None:

    await db_del_league(data=callback.data.split("_")[1])

    result = await db_table_delete(table_name=callback.data.split('_')[1])

    if result:
        await callback.answer(text=f"👍{callback.data.split('_')[1]} deleted from database successfully",
                              show_alert=True
                              )
        logging.info(f'Id: {callback.from_user.id} - Del_league command completed successfully')

    else:
        await callback.answer(text="‼️This league no longer exists. Choose another one",
                              show_alert=True
                              )