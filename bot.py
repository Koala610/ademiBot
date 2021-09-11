import settings
import logging
import re
import markups as nav
import json
import datetime

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
        await state.update_data(login = message.text)
        await States.password.set()
    else:
        await message.answer("Логин неверный")




@dp.message_handler(state = States.password)
async def add_password(message : types.Message,state:FSMContext):
    password = message.text
    if users_db.password_exists(password):
        await message.answer("Вы успешно вошли!")
        state_data = await state.get_data()
        login = state_data.get("login")
        user_id = message.from_user.id
        users_db.update_tg_id(user_id, login)

        """date time"""
        offers = offers_db.get_offers(1000)
        isActual = False
        cur_date = datetime.datetime.now().date()
        for offer in offers:
            offer_start_date = offer[2].split('/')
            offer_finish_date = offer[3].split('/')
            trans_start_date = datetime.date(int(offer_start_date[2]), int(offer_start_date[1]), int(offer_start_date[0]))
            trans_finish_date = datetime.date(int(offer_finish_date[2]), int(offer_finish_date[1]), int(offer_finish_date[0]))
            if cur_date <= trans_finish_date and cur_date >= trans_start_date:
                isActual = True
                break

        """"""

        if isActual:
            nav.mainMenu.add(nav.mealBtn)

        await bot.send_message(message.from_user.id, "Привет {0.first_name}".format(message.from_user), reply_markup = nav.mainMenu)
        await state.finish()
    else:
        await message.answer("Пароль неверный")
    

@dp.message_handler()
async def bot_message(message : types.Message):
    if message.text == "🍍 Еда":
        category = 1000
        offers = offers_db.get_offers(1000)
        cur_offers = []
        cur_date = datetime.datetime.now().date()
        for offer in offers:
            offer_start_date = offer[2].split('/')
            offer_finish_date = offer[3].split('/')
            trans_start_date = datetime.date(int(offer_start_date[2]), int(offer_start_date[1]), int(offer_start_date[0]))
            trans_finish_date = datetime.date(int(offer_finish_date[2]), int(offer_finish_date[1]), int(offer_finish_date[0]))
            if cur_date <= trans_finish_date and cur_date >= trans_start_date:
                cur_offers.append(offer)
                


        await bot.send_message(message.from_user.id, "Список еды")
        for offer in cur_offers:
            result = "<b>Заведение: %s </b>"%(offer[1])
            await bot.send_message(message.from_user.id, result, reply_markup = nav.inline_menu, parse_mode ='HTML')

@dp.callback_query_handler(lambda c: c.data == 'sale_btn')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    





if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)