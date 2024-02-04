from environs import Env

env = Env()   # class instance
env.read_env()  # read .env file, if it exists

BOT_TOKEN = env.str("BOT_TOKEN")  # get a token from .env file in str format
ADMINS = env.list("ADMINS")  # get list of admins from .env file

SITE_TOKEN = env.str("SITE_TOKEN")
SITE_HOST = env.str("SITE_HOST")


DB_NAME = env.str("DB_NAME")
DB_USER = env.str("DB_USER")
DB_HOST = env.str("DB_HOST")
DB_PASSWORD = env.str("DB_PASSWORD")



# TODO instead of AVAILABLE_LEAGUES I should implement league save to and league retrieving from database
AVAILABLE_LEAGUES = {"id_1": "ChampionsShip", "id_2": "Seria A"}
