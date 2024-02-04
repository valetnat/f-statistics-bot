from aiogram import executor, Dispatcher

import logging


from loader import dp, db

from utils.set_default_commands import set_default_commands
from utils.notify_admins import on_start_up_notify, on_shutdown_notify
import handlers


async def on_startup(dp: Dispatcher):
    logging.info('Bot is running')
    await on_start_up_notify(dp)
    await set_default_commands()


# Configure logging
# logging.basicConfig(level=logging.INFO,
#                     format="%(asctime)s %(levelname)s %(message)s")

logging.basicConfig(level=logging.INFO,
                    filename="logging.log",
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    filemode="a"
                    )


async def on_shutdown(dp: Dispatcher):
    await on_shutdown_notify(dp)
    await dp.storage.close()
    if db.is_connected():
        db.commit()
        logging.info("DATABASE COMMIT CHANGES")
        db.close()
        logging.info("DATABASE CONNECTION INTERRUPR")

if __name__ == '__main__':
    import models.models
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)