from aiogram import types, Router
from aiogram.types import Message
from aiogram.filters import Command
import emoji
from src.bin.text import TEXT_HELP, TEXT_WELCOME
from src.bin.utils import get_article_address
from src.bin.bot.class_DB import DataBase
from aiogram.enums.dice_emoji import DiceEmoji
# from src.bin.storage import write_article_in_db
# from src.bin.Exceptions import decorator_exceptions

router = Router()
dict_with_users = {}


@router.message(Command("start", 'help'))
async def start_handler(message: Message):
    if message.text == '/start':
        await message.answer(TEXT_WELCOME)
        if not (message.from_user.id in dict_with_users.keys()):
            dict_with_users[message.from_user.id] = DataBase(message.from_user.id)
    await message.answer(TEXT_HELP)


@router.message(Command("dice"))
async def cmd_dice(message: Message):
    await message.answer(text="Выберите вашу роль." + emoji.emojize(":brain:"))
    print(dict_with_users.get(message.from_user.id).id_user)


@router.message(Command('get_article'))
async def get_article(message: types.Message):
    database_for_user = dict_with_users.get(message.from_user.id)
    random_article = database_for_user.get_random_article_from_db()

    await message.answer(text=random_article)


@router.message()
async def message_handler(message: Message):
    if message.text.find("http") != -1:
        database_for_user = dict_with_users.get(message.from_user.id)
        article_address = get_article_address(message.text)
        info_about_writing = database_for_user.write_article_in_db(article_address)
        await message.answer(info_about_writing, disable_web_page_preview=True)
