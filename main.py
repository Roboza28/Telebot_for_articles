# -*- coding: utf-8 -*-
from settings import TOKEN
import telebot

from src.bin.Exceptions import decorator_exceptions
from src.bin.storage import get_random_article_from_db, write_article_in_db
from src.bin.msg_for_user import TEXT_WELCOME, TEXT_HELP
from src.bin.service import get_article_address
from telebot import types

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: types.Message) -> None:
    if message.text == '/start':
        bot.send_message(message.chat.id, TEXT_WELCOME)

    bot.send_message(message.chat.id, TEXT_HELP)


@bot.message_handler(commands=['get_article'])
def get_article(message: types.Message) -> None:
    random_article = get_random_article_from_db(message.from_user.id)
    bot.send_message(message.chat.id, random_article)


@bot.message_handler()
def parce_text_message(message: types.Message) -> None:
    if message.text.find("http") != -1:
        article_address = get_article_address(message.text)
        info_about_writing = write_article_in_db(article_address, message.from_user.id)
        bot.send_message(message.chat.id, info_about_writing)


@decorator_exceptions
def main() -> None:
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
