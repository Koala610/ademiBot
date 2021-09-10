from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


mealBtn = KeyboardButton("🍍 Еда")
mainMenu = ReplyKeyboardMarkup(resize_keyboard = True)

more_info_btn = InlineKeyboardButton("Подробнее", callback_data = "btn1")
sale_btn = InlineKeyboardButton("Получить скидку", callback_data = "sale_btn")
inline_menu = InlineKeyboardMarkup().add(sale_btn, more_info_btn)
