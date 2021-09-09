from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

mealBtn = KeyboardButton("🍍 Еда")
mainMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(mealBtn)