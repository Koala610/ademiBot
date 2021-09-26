from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_two_btn_menu(text1, callback_data1, text2, callback_data2):
    btn1 = InlineKeyboardButton(text1, callback_data = callback_data1)
    btn2 = InlineKeyboardButton(text2, callback_data = callback_data2)
    menu = InlineKeyboardMarkup().add(btn1, btn2)
    return menu


inline_btn_switch = {
    'reg' :{
        'text' : 'Мои регистрации',
        'callback_header': 'profile_btn::' 
    },
    'ret':{
        'text' : 'Получить деньги',
        'callback_header': 'return::' 

    },
    'sale':{
        'text' : 'Получить скидку',
        'callback_header': 'sale_btn::' 

    }
}


def get_inline_btn(b_id, offer_id, num = None):
    btn_data = inline_btn_switch[b_id]
    btn = InlineKeyboardButton(btn_data['text'], callback_data = btn_data['callback_header']+offer_id) if num == None else InlineKeyboardButton(btn_data['text'], callback_data = btn_data['callback_header']+offer_id+"::"+str(num))
    return btn
    



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
profile_menu = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True, row_width = 2).add(new_offers_btn, offers_taken_btn, offers_processing_btn, offers_done_btn)

admin_req_btn = KeyboardButton("⏳ Запросы")
support_btn = KeyboardButton("👤 Поддержка")
admin_menu = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True, row_width = 2).add(admin_req_btn, support_btn)

login_button = KeyboardButton("🚪 Войти")
login_menu = ReplyKeyboardMarkup(resize_keyboard = True).add(login_button)

exit_button = KeyboardButton("🚪 Выйти")
exit_menu = ReplyKeyboardMarkup(resize_keyboard = True).add(exit_button)


empty_mkp = ReplyKeyboardMarkup()

#btn1 = InlineKeyboardButton("Мои регистрации", callback_data = "profile_btn" + str(offer_id))
#menu = InlineKeyboardMarkup().add(btn1)




