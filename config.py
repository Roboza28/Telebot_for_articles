# -*- coding: utf-8 -*-
from os.path import realpath, dirname
from os import getenv
from os.path import join
from dotenv import load_dotenv

load_dotenv()


TOKEN = getenv('TOKEN')
DEFAULT_DB_NAME = getenv('DEFAULT_DB_NAME')
HOST = getenv('HOST')
USER = getenv('USER')
PASSWORD = getenv('PASSWORD')
PORT = getenv('PORT')
USER_LANGUAGE = getenv('USER_LANGUAGE')
USER_ENCODING = getenv('USER_ENCODING')

PATH_TO_ROOT_FOLDER = dirname(realpath(__file__))

NAME_FOLDER_RESOURCE_PROJECT = 'src'
NAME_FOLDER_WITH_MODULS = 'bin'
NAME_FOLDER_LOG_FILES = 'logs_files'
DB_NAME = 'database_with_articles_users'

PATH_TO_LOG_FILES = join(PATH_TO_ROOT_FOLDER, NAME_FOLDER_RESOURCE_PROJECT, NAME_FOLDER_LOG_FILES)
PATH_TO_DB_FILE = join(PATH_TO_LOG_FILES, DB_NAME)

NAME_COLUMN_TABLES_IN_DB = 'articles'
