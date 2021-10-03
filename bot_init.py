import logging
import settings
import re
import markups as nav
import json
import datetime

from importlib import reload
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


#уровень логов
logging.basicConfig(level = logging.INFO)

#init
storage = MemoryStorage()
bot = Bot(token = settings.API_TOKEN)
dp = Dispatcher(bot, storage = storage)

BOT_STORAGE_LINK = "https://api.telegram.org/file/" + settings.API_TOKEN + "/"



users_db = SQLighter(settings.connection)
offers_db = Offers_model(settings.connection)
requests_db = Req_sql(settings.connection)
admins_db = Admin_sqliter(settings.connection)

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