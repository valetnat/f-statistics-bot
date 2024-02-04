import logging
import mysql.connector

from mysql.connector import errorcode
from data import config
from loader import db, cursor

DB_NAME: str = config.DB_NAME

TABLES: dict = dict()

TABLES['user'] = (
    "CREATE TABLE `user` ("
    "   `id` INT NOT NULL AUTO_INCREMENT,"
    "   `tg_user_id` BIGINT NOT NULL,"
    "   `is_admin` TINYINT NOT NULL DEFAULT 0,"
    "   `full_name` VARCHAR(25) NOT NULL,"
    "   `user_timezone` VARCHAR(25) NOT NULL DEFAULT 'Etc/GMT-3',"
    "   `reg_date` DATETIME NOT NULL,"
    "   PRIMARY KEY (`id`), "
    "   UNIQUE KEY `tg_user_id` (`tg_user_id`),"
    "   KEY `full_name`(`full_name`),"
    "   KEY `is_admin`(`is_admin`)"
    ")  ENGINE=InnoDB")

TABLES['leagues'] = (
    "CREATE TABLE `leagues` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `league_name` VARCHAR(25) NOT NULL,"
    "  `league_id` INT NOT NULL,"
    "  `country_name` VARCHAR(25) NOT NULL,"
    "  `country_id` INT NOT NULL,"
    "  `league_type` VARCHAR(25) NOT NULL,"
    "  `league_sub_type` VARCHAR(25) NOT NULL,"
    "  `added_by` VARCHAR(25) NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  UNIQUE KEY (`league_name`)" 
    ") ENGINE=InnoDB")

TABLES['history'] = (
    "CREATE TABLE `history` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `user_id` BIGINT NOT NULL,"
    "  `name_request` VARCHAR(25) NOT NULL ,"
    "   `create_date` DATETIME NOT NULL,"
    "   PRIMARY KEY (`id`),"
    "   KEY `name_request`(`name_request`),"
    "   KEY `create_date`(`create_date`)"
    # "   FOREIGN KEY (`user_id`) REFERENCES `user` (`tg_user_id`)"
    # "   UNIQUE (`user_id`)"
    ") ENGINE=InnoDB")


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))


try:
    cursor.execute("USE {}".format(DB_NAME))
    print(f"Database {DB_NAME} is using.")
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        db.database = DB_NAME

        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("Table {} already exists".format(table_name))
                else:
                    print(err.msg)
            else:
                print("OK")
    else:
        print(err)


if not __name__ == "__main__":
    logging.info(f"Importing module {__name__}")