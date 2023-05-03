import sqlite3
from sqlite3 import Error
from pathlib import Path
import game_constants

conn = sqlite3.connect(game_constants.NAME_DATA_BASE)
cursor = conn.cursor()


def create_connection():
    """
    Creates a database connection to a SQLite database
    """
    conn = None
    try:
        conn = sqlite3.connect(game_constants.NAME_DATA_BASE)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def connection_exists() -> Path:
    """
    Checks if connection exists

    :return: Path corresponding to location of database. If database does not exist, None is returned
    """
    return Path(game_constants.NAME_DATA_BASE)


def create_table() -> None:
    """
    Creates table in database
    """
    create_table_query = 'CREATE TABLE PLAYERS(name TEXT PRIMARY KEY, score INTEGER not null)'
    execute_query(create_table_query)


def execute_query(query: str) -> None:
    """
    Executes given database query

    :param query: Query to be executed
    """
    cursor.execute(query)
    conn.commit()


def drop_table() -> None:
    """
    Drops table in database
    """
    create_table_query = 'DROP TABLE PLAYERS'
    execute_query(create_table_query)


def insert_player(player_name: str) -> None:
    """
    Inserts player into database

    :param player_name: Name of player, which is added in the database
    """
    insert_player_query = "INSERT INTO PLAYERS (name, score) VALUES('{}', {})".format(player_name, 0)
    execute_query(insert_player_query)


def fetch_data() -> list:
    """
    Fetches data (name and score) from database
    :return: List containing all available names and corresponding scores
    """
    select_data_query = "SELECT * FROM PLAYERS"
    execute_query(select_data_query)
    return cursor.fetchall()


def update_player(player_name: str, score_count: int) -> None:
    """
    Update score of player corresponding to given name

    :param player_name: Name of player, which is updated
    :param score_count: New score of player
    """
    update_player_query = "UPDATE PLAYERS SET score = {} WHERE name = '{}'".format(score_count, player_name)
    execute_query(update_player_query)


def add_new_player(player_name: str) -> None:
    """
    Adds a player corresponding to given name to the database

    :param player_name: Name of player to be added to the database
    """
    # player_name is not yet registered in the db, insert it
    if not player_exists(player_name):
        insert_player(player_name)


def check_scores(player_name: str, score_count: int) -> None:
    """
    Check scores of player, score of player is updated if it is higher than the previous one

    :param player_name: Name of player of which the score is checked
    :param score_count: Score to be checked
    """
    # Only update the player-score if the new score is higher than the previous one
    if fetch_player_score(player_name) < score_count:
        update_player(player_name, score_count)


def is_high_score(player_name: str, score_count: int) -> str:
    """
    Checks if player reached a new personal or general highscore (or nothing)

    :param player_name: Name of player to be checked
    :param score_count: Score which is reached and checked
    :return: Personalised string, depending on if personal/ general highscore has been reached
    """
    if score_count > fetch_high_score():
        return 'Woow Congrats NEW HIGHSCORE: {}'.format(score_count)
    elif score_count > fetch_player_score(player_name):
        return 'Congrats, NEW PERSONAL HIGHSCORE: {}'.format(score_count)
    return ''


def fetch_high_score() -> int:
    """
    Fetches the highest score from database

    :return: Highest score in database
    """
    fetch_max_score_query = "SELECT MAX(score) AS maxScore FROM PLAYERS"
    execute_query(fetch_max_score_query)
    rows = cursor.fetchall()
    return rows[0][0]


def player_exists(player_name: str) -> bool:
    """
    Checks if given player name exists within database

    :param player_name: Name of player to be searched
    :return: True if player exists within database. False if not
    """
    lookup_player_name_query = "SELECT * FROM PLAYERS WHERE name = '{}'".format(player_name)
    cursor.execute(lookup_player_name_query)

    return len(cursor.fetchall()) != 0


def fetch_player_score(player_name: str) -> int:
    """
    Fetches score of given player name

    :param player_name: Name of player to be searched
    :return: Score of player corresponding to passed name
    """
    fetch_player_score_query = "SELECT * FROM PLAYERS WHERE name = '{}'".format(player_name)
    cursor.execute(fetch_player_score_query)

    return cursor.fetchall()[0][1]


def set_up_db() -> None:
    """
    Sets up database if it does not already exist
    """
    if not connection_exists():
        create_table()
