# -*- coding: utf-8 -*-
import psycopg2
import requests
import sqlalchemy
import telebot


class Error(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'{self.message}'


class WrongEmptyName(Error):
    pass


def decorator_exceptions(func):
    """ Функция-декоратор для удобной обработки исключений. """
    def wrapper(*args, **kwargs):
        try:
            result_func = func(*args, **kwargs)

        except WrongEmptyName as custom_err:
            print(f'\nОШИБКА: {custom_err}')

        except ConnectionError as connect_err:
            print(f'\nОШИБКА: {connect_err}')

        except FileNotFoundError:
            print('\nОШИБКА: Данный файл или каталог отсутствует. Сделайте запрос и повторите команду.')

        except PermissionError:
            print('\nОШИБКА: Вам отказано в доступе к файлу истории или он уже открыт в другом приложении.')

        except (psycopg2.OperationalError, sqlalchemy.exc.OperationalError) as db_error:
            print(f'\n{db_error}')

        except psycopg2.errors.DuplicateDatabase as db_duplicate_error:
            print(f'\n{db_duplicate_error}')

        except telebot.apihelper.ApiTelegramException as tg_error:
            print(f'\nОШИБКА:\n{tg_error}')

        except requests.exceptions.ConnectionError:
            print('\nОШИБКА: Нет доступа к интернету.')

        except KeyboardInterrupt:
            print('\nПринудительное прерывание программы.\nПожалуйста, попробуйте еще раз.')

        except Exception as exception:
            print(f'\n{exception}\nПожалуйста, попробуйте еще раз.')

        else:
            return result_func

    return wrapper
