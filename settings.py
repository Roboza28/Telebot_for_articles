# -*- coding: utf-8 -*-
from os.path import join, realpath, dirname
from private import token

TOKEN = token

PATH_TO_ROOT_FOLDER = dirname(realpath(__file__))

USER_LANGUAGE = 'ru'
USER_UNITS = 'metric'
USER_ENCODING = 'utf-8'

NAME_FOLDER_RESOURCE_PROJECT = 'src'
NAME_FOLDER_WITH_MODULS = 'bin'
NAME_FOLDER_LOG_FILES = 'logs_files'

NAME_BD_FILE = 'database_with_articles_users.db'
PATH_TO_DB_FILE = join(PATH_TO_ROOT_FOLDER, NAME_FOLDER_RESOURCE_PROJECT, NAME_FOLDER_LOG_FILES, NAME_BD_FILE)
PATH_TO_LOG_FILES = join(PATH_TO_ROOT_FOLDER, NAME_FOLDER_RESOURCE_PROJECT, NAME_FOLDER_LOG_FILES)

NAME_TABLE_IN_DB = 'Articles_Vava'

NAME_COLUMN_TABLES_IN_DB = 'articles'
