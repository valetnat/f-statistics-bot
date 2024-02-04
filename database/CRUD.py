import mysql.connector
import datetime
import logging
from typing import Optional, Dict, List, Tuple

from aiogram import types
from loader import db, cursor
from mysql.connector import errorcode


def db_available_leagues() -> Optional[List[dict]]:
    try:
        leagues: list = []
        query = """ SELECT * 
                    FROM `leagues`; """
        cursor.execute(query)

        for league in cursor:
            leagues.append(league)

        logging.info(f"SQL query <{db_available_leagues.__name__}> completed successfully")

        return leagues

    except mysql.connector.Error as error:
        logging.error(msg=f"SQL query <{db_available_leagues.__name__}> error: {error}")

        return None


async def db_add_league(data: List, user_id: int) -> bool:
    try:
        query = """ INSERT INTO `leagues`
                    (`league_name`,
                     `league_id`, 
                     `country_name`, 
                     `country_id`, 
                     `league_type`, 
                     `league_sub_type`, 
                     `added_by`) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s); """

        tuple_data = (data[1], data[2], data[3], data[4], data[5], data[6], user_id)
        cursor.execute(query, tuple_data)
        db.commit()
        logging.info(f"SQL query <{db_add_league.__name__}> completed successfully")

        return True

    except mysql.connector.Error as error:
        logging.error(msg=f"SQL query <{db_add_league.__name__}>: {error}")

        return False


async def db_add_teams(table_name: str, data: Dict) -> None:
    try:
        for elem in data.values():
            query = """ INSERT INTO `{table_name}` 
                        (`team_id`,
                         `team_name`,
                         `country_id`,
                         `country_name`)
                         VALUES (%s, %s, %s, %s); """.format(table_name=table_name)

            tuple_data = (elem['team_id'], elem['team_name'], elem['country_id'], elem['country_name'])
            cursor.execute(query, tuple_data)

        db.commit()
        logging.info(f"SQL query <{db_add_teams.__name__}> completed successfully")

    except mysql.connector.Error as error:
        logging.error(msg=f"SQL query <{db_add_teams.__name__}>: {error}")


async def db_get_teams(table_name: str, team_name_1: str, team_name_2: str) -> Optional[Dict]:
    try:
        query: str = """ SELECT * 
                         FROM `{table_name}` 
                         WHERE (
                         (`team_name` = %s) OR (`team_name` = %s)); """. format(table_name=table_name)
        tuple_data = (team_name_1, team_name_2)
        cursor.execute(query, tuple_data)

        teams: Dict[str, int] = dict()

        for team in cursor:
            teams.update({team['team_name']: team['team_id']})

        logging.info(f"SQL query <{db_get_teams.__name__}> completed successfully")

        return teams

    except mysql.connector.Error as error:
        logging.error(msg=f"SQL query <{db_get_teams.__name__}>: {error}")

        return None


async def db_create_league_table(name: str) -> None:
    try:
        query = """ CREATE TABLE `{name}` 
                    (`id` INT NOT NULL AUTO_INCREMENT, 
                     `team_id` INT NOT NULL, 
                     `team_name` VARCHAR(25) NOT NULL, 
                     `country_id` INT NOT NULL,
                     `country_name` VARCHAR(25) NOT NULL,
                     PRIMARY KEY (`id`),
                     UNIQUE KEY `team_id` (`team_id`),
                     KEY `team_name`(`team_name`),
                     KEY `country_name`(`country_name`),
                     KEY `country_id`(`country_id`)) 
                     ENGINE=InnoDB; """.format(name=name)

        cursor.execute(query)
        db.commit()

        logging.info(f"SQL query <{db_create_league_table.__name__}> completed successfully")

    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            logging.error(msg=f"SQL query <{db_create_league_table.__name__}>: {error}")
            print('Table {name} created'.format(name=name))
        else:
            logging.error(msg=f"SQL query <{db_create_league_table.__name__}>: {error}")


async def db_del_league(data: str) -> None:
    try:
        query = " DELETE FROM `leagues` WHERE `league_name` = '{league_name}';".format(league_name=data)
        cursor.execute(query)
        db.commit()

        # query = """ DELETE FROM `leagues`
        #             WHERE `league_name` = %s; """
        #
        # data_tuple = tuple(data)
        # cursor.execute(query, data_tuple)
        db.commit()
        logging.info(f"SQL query <{db_del_league.__name__}> completed successfully")

    except mysql.connector.Error as error:
        logging.error(msg=f"SQL query <{db_del_league.__name__}>: {error}")


async def db_table_delete(table_name: str) -> bool:
    try:
        query = """ DROP TABLE `{table_name}`; """.format(table_name=table_name)
        cursor.execute(query)
        db.commit()

        logging.info(f"SQL query <{db_table_delete.__name__}> completed successfully")

        return True

    except mysql.connector.Error as error:
        logging.error(msg=f"SQL query <{db_table_delete.__name__}>: {error}")

        return False


async def get_users() -> Optional[Tuple]:
    try:
        users = list()
        query = """ SELECT `tg_user_id` FROM `user`; """
        cursor.execute(query)

        for user in cursor:
            users.append(user['tg_user_id'])

        logging.info(f"SQL query <{get_users.__name__}> completed successfully")

        return tuple(users)

    except mysql.connector.Error as error:
        logging.error(msg=f"SQL query <{get_users.__name__}>: {error}")

        return None


async def get_user_timezone(user_id: int) -> str:
    try:
        query = """ SELECT `user_timezone` 
                    FROM `user` 
                    WHERE `tg_user_id`= {user_id}; """.format(user_id=user_id)

        cursor.execute(query)

        logging.info(f"SQL query <{get_user_timezone.__name__}> completed successfully")

        return cursor.fetchall()[0]['user_timezone']

    except mysql.connector.Error as error:
        logging.error(msg=f"SQL query <{get_user_timezone.__name__}>: {error}")


def add_user(data: types.Message, is_admin: int) -> None:
    try:
        query = """ INSERT INTO `user`
                (`tg_user_id`,
                 `is_admin`,
                 `full_name`,
                 `reg_date`)
                 VALUES (%s, %s, %s, %s); """

        data_tuple = (int(data.from_user.id), is_admin, data.from_user.full_name, str(datetime.datetime.now()))
        cursor.execute(query, data_tuple)
        db.commit()

        logging.info(f"SQL query <{add_user.__name__}> completed successfully")

    except mysql.connector.Error as error:
        logging.error(msg=f"SQL query <{add_user.__name__}>: {error}")


async def update_user(data: types.Message, is_admin: int) -> None:
    try:
        query = """ UPDATE `user` 
                    SET `is_admin`= %s 
                    WHERE `tg_user_id`= %s; """

        data_tuple = (is_admin, data.from_user.id)
        cursor.execute(query, data_tuple)
        db.commit()

        logging.info(f"SQL query <{update_user.__name__}> completed successfully")

    except mysql.connector.Error as error:
        logging.error(msg=f"SQL query <{update_user.__name__}>: {error}")


async def update_user_timezone(data: types.Message, user_timezone: str) -> None:
    try:
        query = """ UPDATE `user`
                    SET `user_timezone`= %s 
                    WHERE `tg_user_id`= %s """

        data_tuple = (user_timezone, data.from_user.id)
        cursor.execute(query, data_tuple)
        db.commit()
        logging.info(f"SQL query <{update_user_timezone.__name__}> completed successfully")

    except mysql.connector.Error as error:
        logging.error(msg=f"SQL query <{update_user_timezone.__name__}>: {error}")


async def add_query(user_id: int, query_type: str) -> None:
    try:
        query = """ INSERT INTO `history`
                    (`user_id`,
                     `name_request`,
                     `create_date`)
                     VALUES (%s, %s, %s); """

        data_tuple = (user_id, query_type, datetime.datetime.today())
        cursor.execute(query, data_tuple)
        db.commit()

        logging.info(f"Query: {query_type} - Added into `history` table successfully")

    except mysql.connector.Error as error:
        logging.error(f"Query: {query_type}: {error}")