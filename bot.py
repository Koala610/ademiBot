import settings
import logging
import re
import markups as nav

from importlib import reload

from states import States
from sqliter import SQLighter

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

db = SQLighter(settings.db_path)

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
    if db.user_exists(message.text):
        await message.answer("Введите пароль:")
        await States.password.set()
    else:
        await message.answer("Логин неверный")

@dp.message_handler(state = States.password)
async def add_password(message : types.Message,state:FSMContext):
    password = message.text
    if db.password_exists(password):
        await message.answer("Вы успешно вошли!")
        await bot.send_message(message.from_user.id, "Привет {0.first_name}".format(message.from_user), reply_markup = nav.mainMenu)
        await state.finish()
    else:
        await message.answer("Пароль неверный")
    

@dp.message_handler()
async def bot_message(message : types.Message):
    if message.text == "🍍 Еда":
        await bot.send_message(message.from_user.id, "Список еды")





if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)