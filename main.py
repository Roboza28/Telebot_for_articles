# -*- coding: utf-8 -*-
from src.bin.storage import get_random_article_from_db, write_article_in_db
from src.bin.msg_for_user import TEXT_WELCOME, TEXT_HELP
from src.bin.Exceptions import decorator_exceptions
from src.bin.service import get_article_address
from settings import TOKEN
from telebot import types
import telebot

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
@decorator_exceptions
def start(message: types.Message) -> None:
    if message.text == '/start':
        bot.send_message(message.chat.id, TEXT_WELCOME)

    bot.send_message(message.chat.id, TEXT_HELP)


@bot.message_handler(commands=['get_article'])
@decorator_exceptions
def get_article(message: types.Message) -> None:
    random_article = get_random_article_from_db(message.from_user.id)
    bot.send_message(message.chat.id, random_article)


@bot.message_handler()
@decorator_exceptions
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
