from db_services import *


@dp.message_handler(lambda message: message.text and 
                    (message.text == '/start' or message.text == '🚪 Войти'))
async def login(message: types.Message):
    user_id = message.from_user.id
    message_id = message.message_id
    if users_db.tg_id_exists(user_id) and \
       not users_db.check_if_new(message.from_user.id):
        await show_profile(message)
    else:
        message_list = []
        await dp.storage.update_data(msg_list=message_list, user=user_id)

        del_message = await bot.send_message(user_id, "Введите логин:")
        dlm_id = del_message.message_id
        await add_message_to_dl(message_id, user_id)
        await add_message_to_dl(dlm_id, user_id)

        await States.first()





def get_age(birth_date):
    cur_date = datetime.datetime.now().date()
    res = cur_date - birth_date
    age = int(res.days/365.2)
    return age

def _get_request_markup(menu, id, message_id):
    header = "status_btn::" + str(id) + "::"
    header1_part = header + "1" + '::'
    header2_part = header + "-1" +'::'
    callback_data1 = header1_part + message_id
    callback_data2 = header2_part + message_id
    accept_btn = InlineKeyboardButton("Принять", callback_data = callback_data1)
    reject_btn = InlineKeyboardButton("Отклонить", callback_data = callback_data2)
    menu.add(accept_btn, reject_btn)
    return menu

def _get_request_string_info(request):
    result = "Nickname: " + request[2] + '\n'
    result += "Offer id: " + str(request[3]) + '\n'
    result += "Business: " + get_business_name(request[3]) + '\n'
    result += request_status_switch[int(request[7])]
    return result


def _get_profile_data_str(info, age):
    info_str = "Личные данные" + "\n" 
    info_str += "Логин: " + info[1] + "\n"
    info_str += "Имя: " + info[9] + "\n" if info[9] != None else "Имя: " + " " + "\n"
    info_str += "Фамилия: " + info[10] + "\n" if info[10] != None else "Фамилия: " + " " + "\n"
    info_str += "Возраст: " + str(age) + '\n'
    info_str += "Пол: " + "Мужской" + '\n' if info[11] else "Пол: " + "Женский" + '\n'
    return info_str




async def send_multi_media_message(file_ids, user_id, text, reply_markup):
    media = [InputMediaPhoto(media = file_id) for file_id in file_ids]
    await bot.send_media_group(user_id, media = media)
    await bot.send_message(user_id, text, reply_markup = reply_markup)

async def show_succ_message(src, state=None, is_new=True):
    user_id = src.from_user.id
    if is_new:
        users_db.make_old(user_id)
    await bot.send_message(user_id, "Вы успешно вошли!")
    await bot.send_message(user_id, "Добро пожаловать!")
    await show_profile(src=src)
    if state != None:
        await state.finish()
    await dp.storage.close()

async def show_admin_panel(src):
    if admins_db.check_if_exists(src.from_user.id):
        await bot.send_message(src.from_user.id, "...", reply_markup=admin_menu)
    else:
        await bot.send_message(src.from_user.id, "У вас нет доступа к этому разделу...")

async def show_admin_reqs(src):
    if admins_db.check_if_exists(src.from_user.id):
        await get_requests(src)
    else:
        await bot.send_message(src.from_user.id, "У вас нет доступа к этому разделу...")

async def show_notification_panel(src):
    user_id = src.from_user.id
    if admins_db.check_if_exists(user_id):
        await bot.send_message(user_id, "Выберите действие:", reply_markup=not_menu)
    else:
        await bot.send_message(user_id, "У вас нет доступа к этому разделу...")

async def show_menu(src, text):
    tg_id = src.from_user.id
    main_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(profile_btn, new_offers_btn)

    if admins_db.check_if_exists(tg_id):
        main_menu.add(admin_panel_btn)
    await bot.send_message(tg_id, text, reply_markup=main_menu)

   

async def show_offers_taken(src):
    offers_list = get_offers_taken(src)
    if len(offers_list)>0:
        await show_offers(src, offers_list, 'ret')
        return 1
    await bot.send_message(src.from_user.id, "Пусто")
    return 0

async def show_new_offers(src):
    category_id = CATEGORIES[src.text]['id']
    cur_offers = [offer[0] for offer in get_cur_offers(src = src, category_id=category_id)]
    is_message = True if (type(src) == Message) else False

    await bot.send_message(src.from_user.id, "Список преложений:")
    if len(cur_offers) > 0:
        await show_offers(src, cur_offers, 'sale')
    else:
        await bot.send_message(src.from_user.id, "Список пуст") 

async def show_offers(src, offers, cb_header, exist_filter = False):
    user_id = src.from_user.id
    msg_id = str(src.message_id) if type(src) == Message else str(src.message.message_id)
    inl_btn = list(inline_btn_switch[cb_header].values())
    cnt = 0
    for offer in offers:
        if exist_filter and str(offer) in users_db.get_offers_taken(user_id):
            continue
        result, menu = get_offers_info(user_id, msg_id, offer, inl_btn)
        await bot.send_message(user_id, result, reply_markup = menu,  parse_mode ='HTML')
        cnt+= 1
    return cnt


async def find_new_offers(src):
    user_id = src.from_user.id
    new_offers_menu = get_categories_markup_menu(user_id)
    try:
        menu_len = len(
            (dict(new_offers_menu))['keyboard'][0])
    except IndexError:
        await bot.send_message(user_id, "Нет доступных категорий")
    else:
        await bot.send_message(user_id, "Выберите категорию:", reply_markup = new_offers_menu)

async def show_profile(src):
    info = users_db.get_info(src.from_user.id)
    birth_date = info[11]
    age = get_age(birth_date)
    info_str = _get_profile_data_str(info, age)
    await bot.send_message(src.from_user.id, info_str, reply_markup=profile_menu)

async def show_support_win(src):
    user_id = src.from_user.id
    if admins_db.check_if_exists(user_id):
        await bot.send_message(user_id, "Админ")
    else:
        await bot.send_message(user_id, "User")

async def show_proccessing_reqs(src):
    await get_requests(src, status=0)

async def show_finished_reqs(src):
    trigger_one = await get_requests(src, status=1)
    trigger_two = await get_requests(src, status=-1)
    if trigger_one == True and trigger_two == True:
        await bot.send_message(src.from_user.id, "Список пуст")

async def get_requests(src, status = None, return_len = False):
    user_id = src.from_user.id
    message_id = str(src.message_id) if type(src) == Message else str(src.message.message_id)
    requests = get_requests_by_status(status, user_id)
    requests_len = len(requests)
    is_empty = requests_len == 0 or (requests_len == 1 and \
               len(requests[0]) == 0)   
    if is_empty:
        await bot.send_message(src.from_user.id, "Список пуст")
        return True
    for request in requests:
        if len(request) == 0:
            continue
        menu = InlineKeyboardMarkup()
        if status == None and request[7] == 0:
            menu = _get_request_markup(menu, request[0], message_id)
        await send_multi_media_message(
            [request[5], request[6]], user_id, _get_request_string_info(request), menu)
        del menu

async def send_broadcast_notification(src):
    user_id = src.from_user.id
    await bot.send_message(user_id, "Введите IDs, разделённые знаком '/'")
    await Notification_states.id_obtain.set()

async def send_multicast_notification(src):
    pass


async def check_full_fields(src, func=None, text=None):
    user_id = src.from_user.id
    optional_info = users_db.get_optional_info(user_id)
    length = len(optional_info)
    cnt = 0
    for i in range(length):
        if optional_info[i] == None:
            cnt+=1
            if cnt:
                if func != None:
                    await func(user_id, text)

            await bot.send_message(user_id, "Введите " + states_switch[i]['name'] + ":" )
            await states_switch[i]["state"].set()
            return False
    return True