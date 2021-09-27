from db_init import *
from command_proccessing_functions import *
from bot_init import *

#echo

command_switch = {
    "🍍 Еда": show_new_offers,
    "🏃‍ Тренировки":show_new_offers,
    "🎳 Другое":show_new_offers,
    "🔍 Найти предложения": find_new_offers,
    "/offers": find_new_offers,
    "👤 Профиль": show_profile,
    "🔄 Обновить": show_profile,
    "/profile": show_profile,
    "👤 Админ.панель": show_admin_panel,
    "/admin": show_admin_panel,
    "/ad_reqs": show_admin_reqs,
    "⏳ Запросы": show_admin_reqs,
    "/support": show_support_win,
    "👤 Поддержка": show_support_win,
    "☑️ Зарегистрированные": show_offers_taken,
    "⏳ В обработке": show_proccessing_reqs,
    "💲 Завершённые": show_finished_reqs,
    "🔔 Уведомления": show_notification_panel,
    "/notification": show_notification_panel,
    "📢 Отправить всем": send_broadcast_notification,
    "📢 Отправить по категориям": send_multicast_notification,
}



@dp.message_handler(lambda message: message.text and (message.text =='/start' or message.text == '🚪 Войти'))
async def login(message: types.Message):
    if users_db.tg_id_exists(message.from_user.id):
        await show_profile(message)
    else:
        message_list = []
        await dp.storage.update_data(msg_list = message_list, user = message.from_user.id)

        del_message = await bot.send_message(message.from_user.id, "Введите логин:")
        dlm_id = del_message.message_id
        await add_message_to_dl(message.message_id, message.from_user.id)
        await add_message_to_dl(dlm_id, message.from_user.id)

        await States.first()

@dp.message_handler(commands=['menu'])
async def go_to_main_menu(message: types.Message):
    await show_menu(message, "Главное меню")

@dp.message_handler(state = States.login)
async def add_login(message : types.Message,state:FSMContext):
    #hash = hash(message.text)
    if users_db.user_exists(message.text):
        del_message = await bot.send_message(message.from_user.id, "Введите пароль:")
        dlm_id = del_message.message_id
        await add_message_to_dl(dlm_id, message.from_user.id)
        await state.update_data(login = message.text)
        await States.password.set()
    else:
        del_message = await bot.send_message(message.from_user.id, "Логин неверный")
        dlm_id = del_message.message_id
        await add_message_to_dl(dlm_id, message.from_user.id)
    await add_message_to_dl(message.message_id, message.from_user.id)



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


@dp.message_handler(state = States.password)
async def add_password(message : types.Message,state:FSMContext):
    password = message.text
    state_data = await state.get_data()
    login = state_data.get("login")
    if users_db.password_exists(login, password):
        user_id = message.from_user.id
        users_db.update_tg_id(user_id, login)
        dp_data = await dp.storage.get_data(user = message.from_user.id)
        message_list = dp_data.get('msg_list')
        for msg in message_list:
            await bot.delete_message(message.chat.id, msg)
        await bot.delete_message(message.chat.id, message.message_id)

        if not users_db.check_if_new(message.from_user.id):
            await show_succ_message(src = message, state = state, is_new = False)
        else:
            await check_full_fields(message, bot.send_message, "Некоторые поля требуют заполнения...")


        
    else:
        del_message = await bot.send_message(message.from_user.id, "Пароль неверный")
        dlm_id = del_message.message_id
        await add_message_to_dl(dlm_id, message.from_user.id)
        await add_message_to_dl(message.message_id, message.from_user.id)

@dp.message_handler(state = States.name)
async def add_name(message : types.Message,state:FSMContext):
     users_db.update_name(message.from_user.id, message.text)
     if await check_full_fields(message) == True:
        await show_succ_message(message, state = state)

@dp.message_handler(state = States.surname)
async def add_surname(message : types.Message,state:FSMContext):
     users_db.update_surname(message.from_user.id, message.text)
     if await check_full_fields(message) == True:
        await show_succ_message(message, state = state)

@dp.message_handler(state = States.date)
async def add_date(message : types.Message,state:FSMContext):
     users_db.update_date(message.from_user.id, message.text)
     if await check_full_fields(message) == True:
        await show_succ_message(message, state = state)

@dp.message_handler(state = States.gender)
async def add_gender(message : types.Message,state:FSMContext):
     users_db.update_gender(message.from_user.id, message.text)
     if await check_full_fields(message) == True:
        await show_succ_message(message, state = state)




@dp.message_handler(state = Notification_states.message_state)
async def add_notif_message(message : types.Message,state:FSMContext):
    state_data = await state.get_data()
    offers_ids = state_data.get('ids')
    msg = message.text
    user_ids = users_db.get_users_ids()
    detais_menu = InlineKeyboardMarkup()
    if offers_ids != '-1':
        detais_btn = InlineKeyboardButton("Детали", callback_data = "details_btn::"+offers_ids)
        detais_menu.add(detais_btn)
    
    for user_id in user_ids:
        await bot.send_message(chat_id = user_id, text = msg, reply_markup = detais_menu)
    await bot.send_message(message.from_user.id, "Успешно", reply_markup = nav.admin_menu)
    await state.finish()

@dp.message_handler(state = Notification_states.id_obtain)
async def add_ids(message : types.Message,state:FSMContext):
    offers_ids_list = message.text.split('/')
    offers_ids_list = [offer_id for offer_id in offers_ids_list if check_if_offer_exist(offer_id)]
    offers_ids = '/'.join(offers_ids_list)

    if len(offers_ids_list) == 0:
        await bot.send_message(message.from_user.id, "Ошибка... ID не найдены. Повторите")
        return -1
    await bot.send_message(message.from_user.id, "Введите сообщение:")
    await state.update_data(ids = offers_ids)
    await Notification_states.message_state.set()

@dp.callback_query_handler(lambda c: 'details_btn' in c.data)
async def process_callback_details_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    callback_data = callback_query.data
    offers_ids = callback_data.split("::")[1].split('/')
    try:
        offers_cnt = await show_offers(callback_query, offers_ids, 'sale', exist_filter = True)
    except:
        await bot.send_message(callback_query.from_user.id, "Ошибка... Номер заказа не определён", reply_markup = nav.profile_menu)
        return -1
    if offers_cnt == 0:
        await bot.send_message(callback_query.from_user.id, "К сожалению, ничего(", reply_markup = nav.profile_menu)
    elif offers_cnt == -1:
        await bot.send_message(callback_query.from_user.id, "Ошибка", reply_markup = nav.profile_menu)
    else:
        await bot.send_message(callback_query.from_user.id, "...", reply_markup = nav.profile_menu)



@dp.message_handler()
async def bot_message(message : types.Message):
    if users_db.tg_id_exists(message.from_user.id):
        try:
            await command_switch[message.text](message)
        except KeyError:
            return -1
    else:
        await bot.send_message(message.from_user.id, "Вы не авторизованны...", reply_markup = nav.login_menu)






@dp.callback_query_handler(lambda c: 'profile_btn' in c.data)
async def process_callback_profile_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "...", reply_markup = nav.profile_menu)
    await show_offers_taken(callback_query)


@dp.callback_query_handler(lambda c: 'return' in c.data)
async def process_return_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    tg_id = callback_query.from_user.id
    offer_id = callback_query.data.split('::')[1]
    await dp.storage.update_data(user = tg_id, offer_id = offer_id)
    
    await bot.send_message(callback_query.from_user.id, "Введите ссылку на сторис/пост:", reply_markup = nav.exit_menu)
    await Req_states.link.set()

@dp.message_handler(state = Req_states.link)
async def enter_link(message : types.Message,state:FSMContext):
    if message.text == "🚪 Выйти":
        await state.finish()
        await bot.send_message(message.from_user.id, "Успешно", reply_markup= nav.profile_menu)
        return 1
    if "instagram.com/stories" in message.text or "instagram.com/p" in message.text: 
        await state.update_data(link = message.text)
        await bot.send_message(message.from_user.id, "Отправьте скриншот перевода:", reply_markup = nav.exit_menu)
        await Req_states.picture2.set()
    else:
        await bot.send_message(message.from_user.id, "Это не ссылка", reply_markup = nav.exit_menu)
    

@dp.message_handler(content_types=['photo'], state = Req_states.picture2)
async def upload_pic2(message : types.Message,state:FSMContext):
    tg_id = message.from_user.id
    file_id = message.photo[-1].file_id
    await state.update_data(trans_pic = file_id)
    await bot.send_message(message.from_user.id, "Отправьте фото чека...", reply_markup = nav.exit_menu)
    await Req_states.picture.set()

@dp.message_handler(state = Req_states.picture2)
async def upload_pic_text2(message : types.Message,state:FSMContext):
    if message.text == "🚪 Выйти":
        await state.finish()
        await bot.send_message(message.from_user.id, "Успешно", reply_markup= nav.profile_menu)
        return 1



@dp.message_handler(content_types=['photo'], state = Req_states.picture)
async def upload_pic(message : types.Message,state:FSMContext):
    tg_id = message.from_user.id
    login = users_db.get_login(tg_id)
    mem_data = await dp.storage.get_data(user = message.from_user.id)
    offer_id = mem_data.get('offer_id')
    file_id = message.photo[-1].file_id
    state_data = await state.get_data()
    story_link = state_data.get('link')
    trans_pic = state_data.get('trans_pic')
    requests_db.add_request(tg_id, login, offer_id, story_link, file_id, trans_pic)
    try:
        users_db.del_user_offer(tg_id, offer_id)
    except:
        await bot.send_message(message.from_user.id, "Ошибка")
        await state.finish()

    await bot.send_message(message.from_user.id, "Успешно", reply_markup = nav.profile_menu)


    await state.finish()

@dp.message_handler(state = Req_states.picture)
async def upload_pic_text(message : types.Message,state:FSMContext):
    if message.text == "🚪 Выйти":
        await state.finish()
        await bot.send_message(message.from_user.id, "Успешно", reply_markup= nav.profile_menu)
        return 1


@dp.callback_query_handler(lambda c: 'sale_btn' in c.data)
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    callback_data = callback_query.data.split('::')
    offer_id = callback_data[1]
    num_id = 0
    try:
        num_id = callback_data[2]
    except:
        pass
    if offers_db.check_views_limit(offer_id) and not str(offer_id) in users_db.get_offers_taken(callback_query.from_user.id):
        users_db.add_offer(offer_id, callback_query.from_user.id)
        offers_db.increment_views(offer_id)
        await bot.send_message(callback_query.from_user.id, "Вы успешно заняли место", reply_markup = nav.profile_menu)

        if num_id != '2':
            menu = get_two_btn_menu("Мои регистрации", "profile_btn::" + str(offer_id), "Подробнее", "more_btn::" + str(offer_id) + "::" + str(callback_query.message.message_id)+ "::" + str(callback_query.message.chat.id) + "::" +"reg")
        elif num_id == '2':
            reg_btn = InlineKeyboardButton("Мои регистрации", callback_data = "profile_btn::" + str(offer_id))
            menu = InlineKeyboardMarkup().add(reg_btn)
        await callback_query.message.edit_text(callback_query.message.text, reply_markup = menu, parse_mode = "HTML")


    else:
        await bot.send_message(callback_query.from_user.id, "К сожалению, мест нет")


@dp.callback_query_handler(lambda c: 'more_btn' in c.data)
async def show_more_info(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    callback_data = callback_query.data.split('::')
    offer_id = callback_data[1]
    btn_id = callback_data[4]
    btn1 = nav.get_inline_btn(btn_id, offer_id, num = 2)
    menu = InlineKeyboardMarkup().add(btn1)
    bus_name = offers_db.get_business_name(offers_db.get_business_id(offer_id))
    offer = offers_db.get_info(offer_id)
    views_left = str(int(offer['views_limit']) - int(offer['views']))
    result = '<b>' + offer['theme'] + '</b>' + '\n'
    result += "Организатор: "+ bus_name + '\n'
    result += offer['text'] + '\n'
    result += "Начало: " '<i>'+offer['start_date'] + ' ' + offer['start_time'] + '</i>' '\n'
    result += "Конец: " '<i>'+offer['finish_date'] + ' ' + offer['end_time'] + '</i>' '\n'
    result += "Осталось мест: "+views_left+ '\n'
    try:
        await callback_query.message.edit_text(result, reply_markup = menu, parse_mode = "HTML")
    except MessageNotModified:
        pass



    

    





if __name__ == '__main__':
    executor.start_polling(dp)