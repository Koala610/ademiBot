from views import *


@dp.callback_query_handler(lambda c: 'details_btn' in c.data)
async def process_callback_details_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    callback_data = callback_query.data
    offers_ids = callback_data.split("::")[1].split('/')
    try:
        offers_cnt = await show_offers(callback_query, offers_ids, 'sale',
                                       exist_filter=True)
    except:
        await bot.send_message(user_id, "Ошибка... Номер заказа не определён", reply_markup=profile_menu)
        return -1
    if offers_cnt == 0:
        await bot.send_message(user_id, "К сожалению, ничего(", reply_markup=profile_menu)
    elif offers_cnt == -1:
        await bot.send_message(user_id, "Ошибка", reply_markup=profile_menu)
    else:
        await bot.send_message(user_id, "...", reply_markup=profile_menu)


@dp.callback_query_handler(lambda c: 'profile_btn' in c.data)
async def process_callback_profile_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "...", reply_markup=profile_menu)
    await show_offers_taken(callback_query)


@dp.callback_query_handler(lambda c: 'return' in c.data)
async def process_return_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    tg_id = callback_query.from_user.id
    offer_id = callback_query.data.split('::')[1]
    await dp.storage.update_data(user=tg_id, offer_id=offer_id)

    await bot.send_message(callback_query.from_user.id, "Введите ссылку на сторис/пост:", reply_markup=exit_menu)
    await Req_states.link.set()

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
        add_offer(offer_id, callback_query.from_user.id)
        await bot.send_message(callback_query.from_user.id, "Вы успешно заняли место", reply_markup=profile_menu)

        if num_id != '2':
            btn_text1 = "Мои регистрации"
            btn_callback_data1 = "profile_btn::" + str(offer_id)
            btn_text2 = "Подробнее"
            btn_callback_data2 = "more_btn::" + str(offer_id) + "::" + \
                str(callback_query.message.message_id) + "::" + \
                str(callback_query.message.chat.id) + "::" + "reg"
            menu = get_two_btn_menu(
                btn_text1, btn_callback_data1, btn_text2, btn_callback_data2)
        elif num_id == '2':
            reg_btn = InlineKeyboardButton(
                "Мои регистрации", callback_data="profile_btn::" + str(offer_id))
            menu = InlineKeyboardMarkup().add(reg_btn)
        await callback_query.message.edit_text(callback_query.message.text, reply_markup=menu, parse_mode="HTML")


    else:
        await bot.send_message(callback_query.from_user.id, "К сожалению, мест нет")


@dp.callback_query_handler(lambda c: 'more_btn' in c.data)
async def show_more_info(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    callback_data = callback_query.data.split('::')
    offer_id = callback_data[1]
    btn_id = callback_data[4]

    btn1 = get_inline_btn(btn_id, offer_id, num=2)
    menu = InlineKeyboardMarkup().add(btn1)
    bus_name = offers_db.get_business_name(offers_db.get_business_id(offer_id))
    offer = offers_db.get_info(offer_id)
    views_left = str(int(offer['views_limit']) - int(offer['views_count']))
    
    result = '<b>' + offer['theme'] + '</b>' + '\n'
    result += "Организатор: " + bus_name + '\n'
    result += offer['text'] + '\n'
    result += "Начало: " '<i>' + \
        str(offer['start_date']) + ' ' + str(offer['start_time']) + '</i>' '\n'
    result += "Конец: " '<i>' + \
        str(offer['finish_date']) + ' ' + str(offer['end_time']) + '</i>' '\n'
    result += "Осталось мест: "+views_left + '\n'
    try:
        await callback_query.message.edit_text(result, reply_markup=menu, parse_mode="HTML")
    except MessageNotModified:
        pass


@dp.callback_query_handler(lambda c: 'status_btn' in c.data)
async def change_req_status(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    callback_data = callback_query.data.split('::')
    request_id = callback_data[1]
    req_status = requests_db.get_request_status(request_id)
    if req_status == 0:
        action_id = callback_data[2]
        requests_db.change_status(request_id, action_id)
        await bot.send_message(callback_query.from_user.id, "Успех")
        result_msg = "Ваш запрос был "
        result_msg += "одобрен." if action_id == "1" else "отклонён."
        user_id = requests_db.get_request_tg_id(request_id)
        await bot.send_message(user_id, result_msg)
    else:
        await bot.send_message(callback_query.from_user.id, "Запрос уже обработан")