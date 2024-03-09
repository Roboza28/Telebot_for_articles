# -*- coding: utf-8 -*-
import sqlite3

import requests
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
            print(f'\nОШИБКА. {custom_err}')

        except ConnectionError as connect_err:
            print(f'\nОШИБКА. {connect_err}')

        except FileNotFoundError:
            print('\nОШИБКА. Данный файл или каталог отсутствует. Сделайте запрос и повторите команду.')

        except PermissionError:
            print('\nОШИБКА. Вам отказано в доступе к файлу истории или он уже открыт в другом приложении.')

        except telebot.apihelper.ApiTelegramException:
            print('\nОШИБКА. Отсутствует/указан неверный токен. Пожалуйста, обратитесь к разработчику.')

        except requests.exceptions.ConnectionError:
            print('\nОШИБКА. Нет доступа к интернету.')

        except sqlite3.OperationalError:
            print('\nОШИБКА. Невозможно открыть файл базы данных. Возможно путь не найден.')

        except KeyboardInterrupt:
            print('\nПринудительное прерывание программы.\nПожалуйста, попробуйте еще раз.')

        except Exception as exception:
            print(f'\nОШИБКА. {exception}\nПожалуйста, попробуйте еще раз.')

        else:
            return result_func

    return wrapper
