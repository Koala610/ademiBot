import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = os.getenv('API_TOKEN')

logging.basicConfig(level = logging.INFO)

#init
storage = MemoryStorage()
bot = Bot(token = API_TOKEN)
dp = Dispatcher(bot, storage = storage)
BOT_STORAGE_LINK = "https://api.telegram.org/file/" + API_TOKEN + "/"