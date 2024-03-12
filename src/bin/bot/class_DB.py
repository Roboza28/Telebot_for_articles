# -*- coding: utf-8 -*-
from src.bin.text import TEXT_IF_ARTICLE_INCLUDE_IN_DB, TEXT_IF_ARTICLE_ALREADY_EXIST, TEXT_IF_STORAGE_EMPTY
from sqlalchemy import create_engine
from sqlalchemy import URL
import pandas as pd
import numpy as np
import psycopg2
import config


class DataBase:
    def __init__(self, id_user: int):
        self.connection = None
        self.cursor = None
        self.id_user = id_user
        self.user_table_name = self.create_name_table_for_user()

        self.get_connection(config.DEFAULT_DB_NAME)
        if not self.is_exists_db_name():
            self.create_db()
        self.close_db()

        self.get_connection(config.DB_NAME)
        if not self.is_exists_table_name():
            self.create_table_in_db()
        self.close_db()

    def get_connection(self, name_bd: str):
        self.connection = psycopg2.connect(host=config.HOST, user=config.USER, password=config.PASSWORD,
                                           database=name_bd)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def close_db(self):
        self.cursor.close()
        self.connection.close()

    def query(self, query):
        self.cursor.execute(query)

    def create_name_table_for_user(self) -> str:
        return f'{config.NAME_COLUMN_TABLES_IN_DB}_user_{self.id_user}'

    def is_exists_db_name(self) -> bool:
        self.query("SELECT datname FROM pg_database")

        table_records = self.cursor.fetchall()
        table_records = list(map(lambda x: x[0], table_records))

        if config.DB_NAME in table_records:
            return True

    def is_exists_table_name(self) -> bool:
        self.query("SELECT * FROM pg_catalog.pg_tables")

        table_records = self.cursor.fetchall()
        table_records = list(map(lambda x: x[1], table_records))

        if self.user_table_name in table_records:
            return True

    def create_db(self):
        self.query(f"CREATE DATABASE {config.DB_NAME}")

    def create_table_in_db(self):
        self.query(f"CREATE TABLE {self.user_table_name}(articles VARCHAR)")

    def change_type_column(self) -> None:
        self.query(f"ALTER TABLE {self.user_table_name} ALTER COLUMN {config.NAME_COLUMN_TABLES_IN_DB} TYPE varchar;")

    def get_type_column(self) -> str:
        self.query(f"SELECT * FROM {self.user_table_name} LIMIT 0")

        for i in self.cursor.description:
            self.query("SELECT typname FROM pg_type WHERE oid={oid}".format(oid=i[1]))
            return self.cursor.fetchone()[0]

    def find_article_in_db(self, article_address: str) -> pd.DataFrame:
        df_with_articles_from_bd = self.read_articles_in_db()

        df_with_find_article = df_with_articles_from_bd[
            df_with_articles_from_bd[config.NAME_COLUMN_TABLES_IN_DB] == article_address]

        return df_with_find_article

    def read_articles_in_db(self) -> pd.DataFrame:
        url_object = URL.create("postgresql+psycopg2",
                                username=config.USER,
                                password=config.PASSWORD,
                                host=config.HOST,
                                database=config.DB_NAME)

        engine = create_engine(url_object)

        with engine.begin() as connection:
            return pd.read_sql(f"select * from {self.user_table_name}", connection)

    def check_data_type_in_column(self):
        self.get_connection(config.DB_NAME)
        if self.get_type_column() != 'varchar':
            self.change_type_column()
        self.close_db()

    def write_article_in_db(self, article_address: str) -> str:
        self.check_data_type_in_column()

        df_with_articles_from_bd = self.find_article_in_db(article_address)
        if df_with_articles_from_bd.empty:
            df_with_add_article = pd.DataFrame({config.NAME_COLUMN_TABLES_IN_DB: [article_address]})

            url_object = URL.create(
                "postgresql+psycopg2", username=config.USER, password=config.PASSWORD, host=config.HOST,
                database=config.DB_NAME)

            engine = create_engine(url_object)

            with engine.begin() as connection:
                df_with_add_article.to_sql(self.user_table_name, index=False, if_exists='append', con=connection)

            return TEXT_IF_ARTICLE_INCLUDE_IN_DB

        else:
            return TEXT_IF_ARTICLE_ALREADY_EXIST

    def get_random_article_from_db(self) -> str:
        df_with_articles_from_db = self.read_articles_in_db().transpose()

        try:
            popped_row = df_with_articles_from_db.pop(np.random.randint(0, len(df_with_articles_from_db)))
        except KeyError:
            return TEXT_IF_STORAGE_EMPTY
        else:
            df_with_articles_from_db = df_with_articles_from_db.transpose()

            url_object = URL.create(
                "postgresql+psycopg2", username=config.USER, password=config.PASSWORD, host=config.HOST,
                database=config.DB_NAME)
            engine = create_engine(url_object)

            with engine.begin() as connection:
                df_with_articles_from_db.to_sql(self.user_table_name, index=False, if_exists='replace', con=connection)

            return f'\nВы хотели прочитать:\n{popped_row.to_string(header=False, index=False)}' \
                   f'\nСамое время это сделать!'
