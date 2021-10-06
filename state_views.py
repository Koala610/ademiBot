from views import *


@dp.message_handler(state=States.login)
async def add_login(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    message_id = message.message_id
    #hash = hash(message.text)
    if users_db.user_exists(message.text):
        del_message = await bot.send_message(user_id, "Введите пароль:")
        dlm_id = del_message.message_id
        await add_message_to_dl(dlm_id, user_id)
        await state.update_data(login=message.text)
        await States.password.set()
    else:
        del_message = await bot.send_message(user_id, "Логин неверный")
        dlm_id = del_message.message_id
        await add_message_to_dl(dlm_id, user_id)
    await add_message_to_dl(message_id, user_id)



@dp.message_handler(state=States.password)
async def add_password(message: types.Message, state: FSMContext):
    password = message.text
    state_data = await state.get_data()
    login = state_data.get("login")
    if users_db.password_exists(login, password):
        user_id = message.from_user.id
        users_db.update_tg_id(user_id, login)
        dp_data = await dp.storage.get_data(user=message.from_user.id)
        message_list = dp_data.get('msg_list')
        for msg in message_list:
            await bot.delete_message(message.chat.id, msg)
        await bot.delete_message(message.chat.id, message.message_id)

        if not users_db.check_if_new(message.from_user.id):
            await show_succ_message(src=message, state=state, is_new=False)
        else:
            await check_full_fields(message, bot.send_message, "Некоторые поля требуют заполнения...")



    else:
        del_message = await bot.send_message(message.from_user.id, "Пароль неверный")
        dlm_id = del_message.message_id
        await add_message_to_dl(dlm_id, message.from_user.id)
        await add_message_to_dl(message.message_id, message.from_user.id)

@dp.message_handler(state=States.name)
async def add_name(message: types.Message, state: FSMContext):
    users_db.update_name(message.from_user.id, message.text)
    if await check_full_fields(message) == True:
        await show_succ_message(message, state=state)


@dp.message_handler(state=States.surname)
async def add_surname(message: types.Message, state: FSMContext):
    users_db.update_surname(message.from_user.id, message.text)
    if await check_full_fields(message) == True:
        await show_succ_message(message, state=state)


@dp.message_handler(state=States.date)
async def add_date(message: types.Message, state: FSMContext):
    date = [int(data) for data in message.text.split('/')]
    users_db.update_date(message.from_user.id,
                         datetime.date(date[0], date[1], date[2]))
    if await check_full_fields(message) == True:
        await show_succ_message(message, state=state)


@dp.message_handler(state=States.gender)
async def add_gender(message: types.Message, state: FSMContext):
    users_db.update_gender(message.from_user.id, message.text)
    if await check_full_fields(message) == True:
        await show_succ_message(message, state=state)




@dp.message_handler(state=Notification_states.message_state)
async def add_notif_message(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    offers_ids = state_data.get('ids')
    msg = message.text
    user_ids = users_db.get_users_ids()
    detais_menu = InlineKeyboardMarkup()
    if offers_ids != '-1':
        detais_btn = InlineKeyboardButton(
            "Детали", callback_data="details_btn::"+offers_ids)
        detais_menu.add(detais_btn)

    for user_id in user_ids:
        await bot.send_message(chat_id=user_id, text=msg, reply_markup=detais_menu)
    await bot.send_message(message.from_user.id, "Успешно", reply_markup=admin_menu)
    await state.finish()

@dp.message_handler(state=Notification_states.id_obtain)
async def add_ids(message: types.Message, state: FSMContext):
    offers_ids_list = message.text.split('/')
    list_len = len(offers_ids_list)
    is_without_menu = '-1' in offers_ids_list
    trigger = True if is_without_menu and list_len > 1 else False
    offers_ids_list = list(
        set([offer_id for offer_id in offers_ids_list if
             check_if_offer_exist(offer_id)]))
    offers_ids = '/'.join(offers_ids_list) if not trigger else "-1"
    if len(offers_ids) == 0:
        await bot.send_message(message.from_user.id, "Ошибка... ID не найдены. Повторите")
        return -1
    await bot.send_message(message.from_user.id, "Введите сообщение:")
    await state.update_data(ids=offers_ids)
    await Notification_states.message_state.set()


@dp.message_handler(state=Req_states.link)
async def enter_link(message: types.Message, state: FSMContext):
    if message.text == "🚪 Выйти":
        await state.finish()
        await bot.send_message(message.from_user.id, "Успешно", reply_markup=profile_menu)
        return 1
    if "instagram.com/stories" in message.text or "instagram.com/p" in message.text:
        await state.update_data(link=message.text)
        await bot.send_message(message.from_user.id, "Отправьте скриншот перевода:", reply_markup=exit_menu)
        await Req_states.picture2.set()
    else:
        await bot.send_message(message.from_user.id, "Это не ссылка", reply_markup=exit_menu)


@dp.message_handler(content_types=['photo'], state=Req_states.picture2)
async def upload_pic2(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    file_id = message.photo[-1].file_id
    await state.update_data(trans_pic=file_id)
    await bot.send_message(message.from_user.id, "Отправьте фото чека...", reply_markup=exit_menu)
    await Req_states.picture.set()

@dp.message_handler(state=Req_states.picture2)
async def upload_pic_text2(message: types.Message, state: FSMContext):
    if message.text == "🚪 Выйти":
        await state.finish()
        await bot.send_message(message.from_user.id, "Успешно", reply_markup=profile_menu)
        return 1



@dp.message_handler(content_types=['photo'], state=Req_states.picture)
async def upload_pic(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    login = users_db.get_login(tg_id)
    mem_data = await dp.storage.get_data(user=message.from_user.id)
    offer_id = mem_data.get('offer_id')
    file_id = message.photo[-1].file_id
    state_data = await state.get_data()
    story_link = state_data.get('link')
    trans_pic = state_data.get('trans_pic')
    requests_db.add_request(tg_id, login, offer_id,
                            story_link, file_id, trans_pic)
    try:
        users_db.del_user_offer(tg_id, offer_id)
    except:
        await bot.send_message(message.from_user.id, "Ошибка")
        await state.finish()

    await bot.send_message(message.from_user.id, "Успешно", reply_markup=profile_menu)


    await state.finish()

@dp.message_handler(state=Req_states.picture)
async def upload_pic_text(message: types.Message, state: FSMContext):
    if message.text == "🚪 Выйти":
        await state.finish()
        await bot.send_message(message.from_user.id, "Успешно", reply_markup=profile_menu)
        return 1