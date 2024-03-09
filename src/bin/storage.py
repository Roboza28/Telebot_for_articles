# -*- coding: utf-8 -*-
from src.bin.msg_for_user import TEXT_IF_ARTICLE_INCLUDE_IN_DB, TEXT_IF_ARTICLE_ALREADY_EXIST, TEXT_IF_STORAGE_EMPTY
from settings import PATH_TO_DB_FILE, NAME_COLUMN_TABLES_IN_DB, PATH_TO_LOG_FILES
from src.bin.Exceptions import decorator_exceptions
import pandas as pd
import numpy as np
import sqlite3
import os


def get_random_article_from_db(user_id: int) -> str:
    df_with_articles_from_df = read_articles_in_db(user_id).transpose()

    user_table_name = create_name_table_for_user(user_id)

    try:
        popped_row = df_with_articles_from_df.pop(np.random.randint(0, len(df_with_articles_from_df)))

    except KeyError:
        return TEXT_IF_STORAGE_EMPTY

    else:
        df_with_articles_from_df = df_with_articles_from_df.transpose()
        with sqlite3.connect(PATH_TO_DB_FILE) as connection:
            df_with_articles_from_df.to_sql(f"{user_table_name}", index=False, if_exists='replace', con=connection)
        return f'\nВы хотели прочитать:\n{popped_row.to_string(header=False, index=False)}\nСамое время это сделать!'


@decorator_exceptions
def write_article_in_db(article_address: str, user_id: int) -> str:
    df_with_articles_from_bd = find_article_in_db(article_address, user_id)

    user_table_name = create_name_table_for_user(user_id)

    if df_with_articles_from_bd.empty:
        df_with_add_article = pd.DataFrame({NAME_COLUMN_TABLES_IN_DB: [article_address]})
        with sqlite3.connect(PATH_TO_DB_FILE) as connection:
            df_with_add_article.to_sql(f"{user_table_name}", index=False, if_exists='append', con=connection)
        return TEXT_IF_ARTICLE_INCLUDE_IN_DB

    else:
        return TEXT_IF_ARTICLE_ALREADY_EXIST


def find_article_in_db(article_address: str, user_name: int) -> pd.DataFrame:
    df_with_articles_from_bd = read_articles_in_db(user_name)
    df_with_find_article = df_with_articles_from_bd[
        df_with_articles_from_bd[NAME_COLUMN_TABLES_IN_DB] == article_address]

    return df_with_find_article


@decorator_exceptions
def read_articles_in_db(user_id: int) -> pd.DataFrame:
    if not os.path.isfile(PATH_TO_DB_FILE):
        create_db()

    user_table_name = create_name_table_for_user(user_id)

    if not is_exists_table_name(user_table_name):
        create_table_in_db(user_table_name)

    with sqlite3.connect(PATH_TO_DB_FILE) as connection:
        return pd.read_sql(f"select * from {user_table_name}", connection)


def create_name_table_for_user(user_id: int) -> str:
    return f'{NAME_COLUMN_TABLES_IN_DB}_user_{user_id}'


def create_table_in_db(user_table_name: str) -> None:
    df = pd.DataFrame({NAME_COLUMN_TABLES_IN_DB: []})
    with sqlite3.connect(PATH_TO_DB_FILE) as connection:
        df.to_sql(user_table_name, index=False, if_exists='append', con=connection)


def is_exists_table_name(user_table_name: str) -> bool:
    with sqlite3.connect(PATH_TO_DB_FILE) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        list_with_name_tables_in_db = list(map(lambda x: x[0], cursor.fetchall()))
        if user_table_name in list_with_name_tables_in_db:
            return True


@decorator_exceptions
def create_db() -> None:
    if not os.path.exists(PATH_TO_LOG_FILES):
        os.mkdir(PATH_TO_LOG_FILES)

    with sqlite3.connect(PATH_TO_DB_FILE):
        pass


if __name__ == '__main__':
    # us1 = User('Владислав', 'Лухнов', 'alters_raindrop')
    # table_name1 = create_name_table_for_user('12345')
    # table_name1 = 123456
    # print(read_articles_in_db(table_name1))
    # # print(write_article_in_db('https1245', table_name1))
    # print(write_article_in_db('https124567', table_name1))
    # print(get_random_article_from_db(table_name1))
    # pass
    create_db()
