from db_init import *
from bot_init import *


def check_if_offer_exist(offer_id):
    is_exist = False
    try:
        is_exist = int(offer_id) in offers_db.get_all_ids()
    except ValueError:
        return False
    return is_exist



async def show_menu(src, text):
    tg_id = src.from_user.id
    new_offers_btn = KeyboardButton("🔍 Найти предложения")
    profile_btn = KeyboardButton("👤 Профиль")
    main_menu = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True).add(profile_btn, new_offers_btn)

    if admins_db.check_if_exists(tg_id):
        admin_panel_btn = KeyboardButton("👤 Админ.панель")
        main_menu.add(admin_panel_btn)
    await bot.send_message(tg_id, text, reply_markup = main_menu)

async def exit_state(state):
    await state.finish()



async def show_offers_taken(src):
    await bot.send_message(src.from_user.id, "Ваши регистрации")
    offers_list = users_db.get_offers_taken(src.from_user.id)
    if len(offers_list) == 0:
        await bot.send_message(src.from_user.id, "Пусто")

    await show_offers(src, offers_list, 'ret')
    



def get_start_finish_date(start_text, finish_text):
    start_date = start_text.split('/')
    finish_date = finish_text.split('/')
    start_date = datetime.date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
    finish_date = datetime.date(int(finish_date[2]), int(finish_date[1]), int(finish_date[0]))
    return start_date, finish_date

def check_cur_offers(src, category_id, cur_offers = None, return_bool = False):
    offers = offers_db.get_offers(category_id)
    cur_date = datetime.datetime.now().date()
    is_actual = False
    for offer in offers:
        can_be_shown = offers_db.check_views_limit(offer[0])
        if not can_be_shown:
            continue

        start_date, finish_date = offer[2], offer[3]
        if cur_date <= finish_date and cur_date >= start_date and not str(offer[0]) in users_db.get_offers_taken(src.from_user.id):
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
    cur_offers = [offer[0] for offer in check_cur_offers(src = src, cur_offers = [], category_id = category_id)]
    is_message = True if (type(src) == Message) else False

    await bot.send_message(src.from_user.id, "Список преложений:")
    if len(cur_offers) > 0:
        await show_offers(src, cur_offers, 'sale')
    else:
        await bot.send_message(src.from_user.id, "Список пуст") 

async def show_offers(src, offers, cb_header, exist_filter = False):
    inl_btn = list(nav.inline_btn_switch[cb_header].values())
    cnt = 0
    for offer in offers:
        if exist_filter and str(offer) in users_db.get_offers_taken(src.from_user.id):
            continue

        bus_name = offers_db.get_business_name(offers_db.get_business_id(offer))
        msg_id = str(src.message_id) if type(src) == Message else str(src.message.message_id)
        user_id = src.from_user.id
        menu = get_two_btn_menu(inl_btn[0], inl_btn[1] + str(offer), "Подробнее", "more_btn::" + str(offer) + "::" + msg_id + "::" + str(user_id) +inl_btn[2])
        result = "<b>Заведение: %s </b>"%(bus_name) + "\n"
        result += "<b>ID заказа: %s </b>"%(offer)
        await bot.send_message(user_id, result, reply_markup = menu,  parse_mode ='HTML')
        cnt+= 1
    return cnt


async def get_requests(src, status = None):
    requests = []
    accept_btn = None
    reject_btn = None
    if status == None:
        requests = requests_db.get_all_requests()
    else:
        requests = [requests_db.get_users_requests_by_status(src.from_user.id, status)]

    if len(requests) == 0 or (len(requests) == 1 and len(requests[0])==0):
        await bot.send_message(src.from_user.id, "Список пуст")
        return -1
    for request in requests:
        if len(request) == 0:
            continue
        menu = InlineKeyboardMarkup()
        if status == None and request[7] == 0:
            header1_part = "status_btn::"+str(request[0])+"::"+"1"+'::'
            header2_part = "status_btn::"+str(request[0])+"::"+"-1"+'::'
            callback_data1 = header1_part + str(src.message_id) if type(src) == Message else header1_part+str(src.message.message_id)
            callback_data2 = header2_part+str(src.message_id) if type(src) == Message else header2_part+str(src.message.message_id)
            accept_btn = InlineKeyboardButton("Принять", callback_data = callback_data1)
            reject_btn = InlineKeyboardButton("Отклонить", callback_data = callback_data2)
            menu.add(accept_btn, reject_btn)

        result = "Nickname: " + request[2] + '\n'
        result += "Offer id: " + str(request[3]) + '\n'
        result += "Business: " + offers_db.get_business_name(offers_db.get_business_id(request[3])) + '\n'
        if request[7] == 1:
            result += "Status: Accepted"
        elif request[7] == -1:
            result += "Status: Declined"
        elif request[7] == 0:
            result += "Status: In process"

        check_photo = InputMediaPhoto(media = request[5])
        trans_photo = InputMediaPhoto(media = request[6])


        await bot.send_media_group(src.from_user.id, media = [check_photo, trans_photo])
        await bot.send_message(src.from_user.id, result, reply_markup = menu)
        del menu


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
    birth_age = info[11]
    cur_month = '%02d'%(datetime.datetime.now().month)
    cur_day = '%02d'%(datetime.datetime.now().day)
    age_var1 = int(str(datetime.datetime.now().year) + cur_month + cur_day)
    age_var2 = int(str(birth_age.year) + '%02d'%(int(birth_age.month)) + '%02d'%(int(birth_age.day)))
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

async def show_notification_panel(src):
    if admins_db.check_if_exists(src.from_user.id):
        await bot.send_message(src.from_user.id, "Выберите действие:", reply_markup = nav.not_menu)
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


async def send_broadcast_notification(src):
    await bot.send_message(src.from_user.id, "Введите IDs, разделённые знаком '/'")
    await Notification_states.id_obtain.set()

async def send_multicast_notification(src):
    pass

async def check_full_fields(src, func = None, text = None):
    if func != None:
        await func(src.from_user.id, text)
    optional_info = users_db.get_optional_info(src.from_user.id)
    length = len(optional_info)
    for i in range(length):
        if optional_info[i] == None:
            await bot.send_message(src.from_user.id, "Введите " + states_switch[i]['name'] + ":" )
            await states_switch[i]["state"].set()
            return False
    return True

async def show_succ_message(src, state = None, is_new = True):
    if is_new:
        users_db.make_old(src.from_user.id)
    await bot.send_message(src.from_user.id, "Вы успешно вошли!")
    await bot.send_message(src.from_user.id, "Добро пожаловать!")
    await show_profile(src = src)
    if state != None:
        await state.finish()
    await dp.storage.close()
