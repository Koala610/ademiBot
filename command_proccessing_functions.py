from db_init import *
from bot_init import *


async def show_menu(src, text):
    tg_id = src.from_user.id
    new_offers_btn = KeyboardButton("🔍 Найти предложения")
    profile_btn = KeyboardButton("👤 Профиль")
    main_menu = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True).add(profile_btn, new_offers_btn)

    if admins_db.check_if_exists(tg_id):
        admin_panel_btn = KeyboardButton("👤 Админ.панель")
        main_menu.add(admin_panel_btn)
    await bot.send_message(tg_id, text, reply_markup = main_menu)



async def show_offers_taken(src):
    await bot.send_message(src.from_user.id, "Ваши регистрации")
    offers_list = users_db.get_offers_taken(src.from_user.id)
    for offer in offers_list:
        bus_id = offers_db.get_business_id(offer)
        bus_name = offers_db.get_business_name(bus_id)
        msg_id = str(src.message_id) if type(src) == Message else str(src.message.message_id)
        chat_id = str(src.chat.id) if type(src) == Message else str(src.message.chat.id)
        menu = get_two_btn_menu("Получить деньги","return::" + str(offer), "Подробнее", "more_btn::" + str(offer) + "::" + msg_id + "::" + chat_id +"::ret")
        result = "<b>Заведение: %s </b>"%(bus_name) + "\n"
        result += "<b>ID заказа: %s </b>"%(offer)
        await bot.send_message(src.from_user.id, result, reply_markup = menu,  parse_mode ='HTML')
    


def check_cur_offers(src, category_id, cur_offers = None, return_bool = False):
    offers = offers_db.get_offers(category_id)
    cur_date = datetime.datetime.now().date()
    is_actual = False
    for offer in offers:
        can_be_shown = offers_db.check_views_limit(offer[0])
        if not can_be_shown:
            continue

        offer_start_date = offer[2].split('/')
        offer_finish_date = offer[3].split('/')
        trans_start_date = datetime.date(int(offer_start_date[2]), int(offer_start_date[1]), int(offer_start_date[0]))
        trans_finish_date = datetime.date(int(offer_finish_date[2]), int(offer_finish_date[1]), int(offer_finish_date[0]))
        if cur_date <= trans_finish_date and cur_date >= trans_start_date and not str(offer[0]) in users_db.get_offers_taken(src.from_user.id):
            if return_bool:
                is_actual = True
                break
            if cur_offers != None:
                cur_offers.append(offer)
    if return_bool:
        return is_actual
    else:
        return cur_offers


async def show_new_offers(src):
    category_id = CATEGORIES[src.text]['id']
    cur_offers = []
    cur_offers = check_cur_offers(src = src, cur_offers = cur_offers, category_id = category_id)

    await bot.send_message(src.from_user.id, "Список преложений:")
    if len(cur_offers) > 0:
        for offer in cur_offers:
            menu = get_two_btn_menu("Получить скидку", "sale_btn::" + str(offer[0]), "Подробнее", "more_btn::" + str(offer[0]) + "::" + str(src.message_id)+ "::" + str(src.chat.id) +"::sale")
            result = "<b>Заведение: %s </b>"%(offer[1])
            await bot.send_message(src.from_user.id, result, reply_markup = menu, parse_mode ='HTML')
    else:
        await bot.send_message(src.from_user.id, "Список пуст")    


async def get_requests(src, status = None):
    requests = []
    if status == None:
        requests = requests_db.get_all_requests()
    else:
        requests = requests_db.get_users_requests_by_status(src.from_user.id, status)

    for request in requests:
        result = "Nickname: " + request[2] + '\n'
        result += "Offer id: " + str(request[3]) + '\n'
        result += "Business: " + offers_db.get_business_name(offers_db.get_business_id(request[3])) + '\n'
        if status == 1:
            result += "Status: Successfully done"
        elif status == -1:
            result += "Status: Declined"
        elif status == 0:
            result += "Status: In process"


        await bot.send_photo(src.chat.id, photo = request[5], caption = result)

async def add_message_to_dl(message_id, user_id):
    strg = await dp.storage.get_data(user = user_id)
    message_list = strg.get('msg_list')
    message_list.append(message_id)
    await dp.storage.update_data(msg_list = message_list, user = user_id)



async def find_new_offers(src):
    new_offers_menu = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
    is_availible = False
    for category in CATEGORIES:
        if check_cur_offers(return_bool = True, category_id = CATEGORIES[category]['id'], src = src):
            is_availible = True
            new_offers_menu.add(KeyboardButton(category))
    if is_availible:
        await bot.send_message(src.from_user.id, "Выберите категорию:", reply_markup = new_offers_menu)
    else:
        await bot.send_message(src.from_user.id, "Нет доступных категорий")

async def show_profile(src):
    info = users_db.get_info(src.from_user.id)
    birth_age = info[11].split('/')
    cur_month = '%02d'%(datetime.datetime.now().month)
    cur_day = '%02d'%(datetime.datetime.now().day)
    age_var1 = int(str(datetime.datetime.now().year) + cur_month + cur_day)
    age_var2 = int(str(birth_age[2]) + '%02d'%(int(birth_age[1])) + '%02d'%(int(birth_age[0])))
    age_var_res = (str(age_var1 - age_var2))
    age = "".join(list(age_var_res)[0:2])

    info_str = "Личные данные" + "\n" 
    info_str += "Логин: " + info[1] + "\n"
    info_str += "Имя: " + info[9] + "\n" if info[9] != None else "Имя: " + " " + "\n"
    info_str += "Фамилия: " + info[10] + "\n" if info[10] != None else "Фамилия: " + " " + "\n"
    info_str += "Возраст: " + str(age) + '\n'
    info_str += "Пол: " + "Мужской" + '\n' if info[11] else "Пол: " + "Женский" + '\n'    

    await bot.send_message(src.from_user.id, info_str, reply_markup = nav.profile_menu)

async def show_admin_panel(src):
    if admins_db.check_if_exists(src.from_user.id):
        await bot.send_message(src.from_user.id, "...", reply_markup = nav.admin_menu)
    else:
        bot.send_message(src.from_user.id, "У вас нет доступа к этому разделу...")

async def show_admin_reqs(src):
    if admins_db.check_if_exists(src.from_user.id):
        await get_requests(src)
    else:
        bot.send_message(src.from_user.id, "У вас нет доступа к этому разделу...")

async def show_support_win(src):
    if admins_db.check_if_exists(src.from_user.id):
        await bot.send_message(src.from_user.id, "Админ")
    else:
        await bot.send_message(src.from_user.id, "User")

async def show_proccessing_reqs(src):
    await get_requests(src, status = 0)

async def show_finished_reqs(src):
    await get_requests(src, status = 1)
    await get_requests(src, status = -1)