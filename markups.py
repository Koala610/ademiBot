from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_two_btn_menu(text1, callback_data1, text2, callback_data2):
    btn1 = InlineKeyboardButton(text1, callback_data = callback_data1)
    btn2 = InlineKeyboardButton(text2, callback_data = callback_data2)
    menu = InlineKeyboardMarkup().add(btn1, btn2)
    return menu



more_info_btn = InlineKeyboardButton(text = "Подробнее", callback_data = "btn1")
sale_btn = InlineKeyboardButton("Получить скидку", callback_data = "sale_btn")
inline_menu = InlineKeyboardMarkup().add(sale_btn, more_info_btn)



profile_btn = KeyboardButton("👤 Профиль")
refresh_profile_btn = KeyboardButton("🔄 Обновить")
new_offers_btn = KeyboardButton("🔍 Найти предложения")
back_menu_btn = KeyboardButton("Назад")
main_menu = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True, row_width = 2).add(profile_btn, new_offers_btn)

offers_taken_btn = KeyboardButton("☑️ Зарегистрированные")
offers_processing_btn = KeyboardButton("⏳ В обработке")
offers_done_btn = KeyboardButton("💲 Завершённые")
profile_menu = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True, row_width = 2).add(offers_taken_btn, offers_processing_btn, offers_done_btn)

admin_req_btn = KeyboardButton("⏳ Запросы")
support_btn = KeyboardButton("👤 Поддержка")
admin_menu = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True, row_width = 2).add(admin_req_btn, support_btn)

login_button = KeyboardButton("🚪 Войти")
login_menu = ReplyKeyboardMarkup(resize_keyboard = True).add(login_button)


empty_mkp = ReplyKeyboardMarkup()


