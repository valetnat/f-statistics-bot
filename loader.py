from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
import mysql.connector
from mysql.connector import errorcode

from data import config
import filters


# Initialize bot and dispatcher
bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Bind customs filters from package filters
filters.setup(dp)

# Create mySQL connection
try:
    db = mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )

except mysql.connector.Error as exp:
    if exp.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif exp.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(exp)
else:
    cursor = db.cursor(dictionary=True)  # create a cursor that returns rows as dictionaries.
    print("Connect to mySQL established")