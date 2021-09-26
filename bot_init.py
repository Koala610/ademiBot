import logging
import settings
import re
import markups as nav
import json
import datetime

from importlib import reload
from markups import get_two_btn_menu

from states import States
from profile_state import Profile_states
from requests_states import Req_states
from notification_states import Notification_states


from aiogram.utils.exceptions import MessageNotModified
from aiogram.types.message import Message
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


#уровень логов
logging.basicConfig(level = logging.INFO)

#init
storage = MemoryStorage()
bot = Bot(token = settings.API_TOKEN)
dp = Dispatcher(bot, storage = storage)

BOT_STORAGE_LINK = "https://api.telegram.org/file/" + settings.API_TOKEN + "/"

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