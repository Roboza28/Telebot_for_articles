# -*- coding: utf-8 -*-
from src.bin.msg_for_user import TEXT_IF_ARTICLE_INCLUDE_IN_DB, TEXT_IF_ARTICLE_ALREADY_EXIST, TEXT_IF_STORAGE_EMPTY
from settings import NAME_COLUMN_TABLES_IN_DB, HOST, USER, PASSWORD, DEFAULT_DB_NAME, DB_NAME
from sqlalchemy import create_engine
from sqlalchemy import URL
import pandas as pd
import numpy as np
import psycopg2


def get_random_article_from_db(user_id: int) -> str:
    df_with_articles_from_df = read_articles_in_db(user_id).transpose()
    user_table_name = create_name_table_for_user(user_id)

    try:
        popped_row = df_with_articles_from_df.pop(np.random.randint(0, len(df_with_articles_from_df)))

    except KeyError:
        return TEXT_IF_STORAGE_EMPTY

    else:
        df_with_articles_from_df = df_with_articles_from_df.transpose()

        url_object = URL.create(
            "postgresql+psycopg2", username=USER, password=PASSWORD, host=HOST, database=DB_NAME)
        engine = create_engine(url_object)

        with engine.begin() as connection:
            df_with_articles_from_df.to_sql(user_table_name, index=False, if_exists='replace', con=connection)

        return f'\nВы хотели прочитать:\n{popped_row.to_string(header=False, index=False)}\nСамое время это сделать!'


def write_article_in_db(article_address: str, user_id: int) -> str:
    user_table_name = create_name_table_for_user(user_id)

    df_with_articles_from_bd = find_article_in_db(article_address, user_id)

    if get_type_column(user_table_name) != 'varchar':
        change_type_column(user_table_name)

    if df_with_articles_from_bd.empty:
        df_with_add_article = pd.DataFrame({NAME_COLUMN_TABLES_IN_DB: [article_address]})

        url_object = URL.create(
            "postgresql+psycopg2", username=USER, password=PASSWORD, host=HOST, database=DB_NAME)

        engine = create_engine(url_object)

        with engine.begin() as connection:
            df_with_add_article.to_sql(user_table_name, index=False, if_exists='append', con=connection)

        return TEXT_IF_ARTICLE_INCLUDE_IN_DB

    else:
        return TEXT_IF_ARTICLE_ALREADY_EXIST


def find_article_in_db(article_address: str, user_name: int) -> pd.DataFrame:
    df_with_articles_from_bd = read_articles_in_db(user_name)

    df_with_find_article = df_with_articles_from_bd[
        df_with_articles_from_bd[NAME_COLUMN_TABLES_IN_DB] == article_address]

    return df_with_find_article


def read_articles_in_db(user_id: int) -> pd.DataFrame:
    if not is_exists_db_name():
        create_db()

    user_table_name = create_name_table_for_user(user_id)

    if not is_exists_table_name(user_table_name):
        create_table_in_db(user_table_name)

    url_object = URL.create("postgresql+psycopg2",
                            username=USER,
                            password=PASSWORD,
                            host=HOST,
                            database=DB_NAME)

    engine = create_engine(url_object)

    with engine.begin() as connection:
        return pd.read_sql(f"select * from {user_table_name}", connection)


def create_name_table_for_user(user_id: int) -> str:
    return f'{NAME_COLUMN_TABLES_IN_DB}_user_{user_id}'


def create_table_in_db(user_table_name: str) -> None:
    connection = psycopg2.connect(host=HOST, user=USER, password=PASSWORD, database=DB_NAME)
    connection.autocommit = True

    cursor = connection.cursor()
    cursor.execute(f"CREATE TABLE {user_table_name}(articles VARCHAR)")

    cursor.close()
    connection.close()


def is_exists_table_name(user_table_name: str) -> bool:
    with psycopg2.connect(host=HOST, user=USER, password=PASSWORD, database=DB_NAME) as connection:
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM pg_catalog.pg_tables")

            table_records = cursor.fetchall()
            table_records = list(map(lambda x: x[1], table_records))

            if user_table_name in table_records:
                return True


def change_type_column(user_table_name) -> None:
    with psycopg2.connect(host=HOST, user=USER, password=PASSWORD, database=DB_NAME) as connection:
        with connection.cursor() as cursor:

            cursor.execute(f"ALTER TABLE {user_table_name} ALTER COLUMN {NAME_COLUMN_TABLES_IN_DB} TYPE varchar;")


def is_exists_db_name() -> bool:
    with psycopg2.connect(host=HOST, user=USER, password=PASSWORD, database=DB_NAME) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT datname FROM pg_database")

            table_records = cursor.fetchall()
            table_records = list(map(lambda x: x[0], table_records))

            if DB_NAME in table_records:
                return True


def get_type_column(user_table_name: str) -> str:
    with psycopg2.connect(host=HOST, user=USER, password=PASSWORD, database=DB_NAME) as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {user_table_name} LIMIT 0")

            for i in cursor.description:
                cursor.execute("SELECT typname FROM pg_type WHERE oid={oid}".format(oid=i[1]))
                return cursor.fetchone()[0]


def create_db() -> None:
    connection = psycopg2.connect(host=HOST, user=USER, password=PASSWORD, database=DEFAULT_DB_NAME)
    connection.autocommit = True

    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE {DB_NAME}")
    cursor.close()

    connection.close()
