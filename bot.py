import settings
import logging
import re
import markups as nav
import json

from importlib import reload

from states import States
from sqliter import SQLighter
from offers_model import Offers_model

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage






#уровень логов
logging.basicConfig(level = logging.INFO)

#init
storage = MemoryStorage()
bot = Bot(token = settings.API_TOKEN)
dp = Dispatcher(bot, storage = storage)

users_db = SQLighter(settings.users_db_path)
offers_db = Offers_model(settings.offers_db_path)

#echo

"""@dp.message_handler()
async def echo(message : types.Message):
    await message.answer(message.text)
"""


@dp.message_handler(commands=['start'])
async def login(message: types.Message):
    await message.answer("Введите логин:")
    await States.first()

@dp.message_handler(state = States.login)
async def add_login(message : types.Message,state:FSMContext):
    #hash = hash(message.text)
    if users_db.user_exists(message.text):
        await message.answer("Введите пароль:")
        await States.password.set()
    else:
        await message.answer("Логин неверный")

@dp.message_handler(state = States.password)
async def add_password(message : types.Message,state:FSMContext):
    password = message.text
    if users_db.password_exists(password):
        await message.answer("Вы успешно вошли!")
        await bot.send_message(message.from_user.id, "Привет {0.first_name}".format(message.from_user), reply_markup = nav.mainMenu)
        await state.finish()
    else:
        await message.answer("Пароль неверный")
    

@dp.message_handler()
async def bot_message(message : types.Message):
    if message.text == "🍍 Еда":
        category = 1000
        offers = offers_db.get_offers(1000)
        await bot.send_message(message.from_user.id, "Список еды")
        await bot.send_message(message.from_user.id, offers)






if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)