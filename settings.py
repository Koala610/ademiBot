"""
Инициализация баз данных, бота, хранилищ
"""
import logging
import re
import markups as nav
import json
import datetime
import os
import pymysql


from markups import get_two_btn_menu
from states import *
from db import *


from aiogram.utils.exceptions import MessageNotModified
from aiogram.types.message import Message
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InputMediaPhoto
#Инициализация пакетов


API_TOKEN = os.getenv('API_TOKEN')
db_link = os.getenv('JAWSDB_URL')
#Получение переменных из среды


logging.basicConfig(level = logging.INFO)

#init
storage = MemoryStorage()
bot = Bot(token = API_TOKEN)
dp = Dispatcher(bot, storage = storage)
BOT_STORAGE_LINK = "https://api.telegram.org/file/" + API_TOKEN + "/"
#Создание бота и его настройка



s = db_link.split("mysql://")[1].split(':')
db_settings = {}
db_settings['user'] = s[0]
db_settings['password'] = s[1].split('@')[0]
db_settings['host'] = s[1].split('@')[1]
db_settings['port'] = int(s[2].split('/')[0])
db_settings['database'] = s[2].split('/')[1]
db_settings['cursorclass'] = pymysql.cursors.DictCursor

try:
    connection = pymysql.connect(
		host = db_settings['host'],
		port = db_settings['port'],
		user = db_settings['user'],
		password = db_settings['password'],
		database = db_settings['database'],
		cursorclass = db_settings['cursorclass'],
        )

except Exception as ex:
	print(ex)

users_db = User_sqliter(connection)
offers_db = Offers_sqliter(connection)
requests_db = Req_sql(connection)
admins_db = Admin_sqliter(connection)
#Инициализация баз данных


CATEGORIES = {
    "🍍 Еда":
    {
        "id" : 1000,
    },

    "🏃‍ Тренировки":
    {
        "id" : 2000,
    },
    "🎳 Другое":
    {
        "id": 3000,
    }

}


states_switch = {
    0:
    {
        "state": States.name,
        "name": "name",
    },
    1:
    {
        "state": States.surname,
        "name": "surname",
    },
    2:
    {
        "state": States.date,
        "name": "date",
    },
    3:
    {
        "state": States.gender,
        "name": "gender",
    },
}

request_status_switch = {
    0: "Status: In process",
    1: "Status: Accepted",
    -1: "Status: Declined",

}

