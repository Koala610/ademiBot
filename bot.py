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
    "💲 Завершённые": show_finished_reqs
}



@dp.message_handler(lambda message: message.text and (message.text =='/start' or message.text == '🚪 Войти'))
async def login(message: types.Message):
    if users_db.tg_id_exists(message.from_user.id):
        await show_menu(message, "Добро пожаловать!")
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
        await message.answer("Вы успешно вошли!")
        await show_menu(src = message, text = "Добро пожаловать!")
        await state.finish()
        await dp.storage.close()

        
    else:
        del_message = await bot.send_message(message.from_user.id, "Пароль неверный")
        dlm_id = del_message.message_id
        await add_message_to_dl(dlm_id, message.from_user.id)
        await add_message_to_dl(message.message_id, message.from_user.id)

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
    await bot.send_message(callback_query.from_user.id, "...", reply_markup = nav.profile_menu)
    await show_offers_taken(callback_query)


@dp.callback_query_handler(lambda c: 'return' in c.data)
async def process_return_callback(callback_query: types.CallbackQuery):
    tg_id = callback_query.from_user.id
    offer_id = callback_query.data.split('::')[1]
    await dp.storage.update_data(user = tg_id, offer_id = offer_id)
    
    await bot.send_message(callback_query.from_user.id, "Введите ссылку на сторис:")
    await Req_states.link.set()

@dp.message_handler(state = Req_states.link)
async def enter_link(message : types.Message,state:FSMContext):
    if "instagram.com/stories" in message.text or "instagram.com/p" in message.text: 
        await state.update_data(link = message.text)
        await bot.send_message(message.from_user.id, "Отправьте фото чека:")
        await Req_states.picture.set()
    else:
        await bot.send_message(message.from_user.id, "Это не ссылка")
    

@dp.message_handler(content_types=['photo'], state = Req_states.picture)
async def upload_pic(message : types.Message,state:FSMContext):
    tg_id = message.from_user.id
    login = users_db.get_login(tg_id)
    mem_data = await dp.storage.get_data(user = message.from_user.id)
    offer_id = mem_data.get('offer_id')
    file_id = message.photo[-1].file_id
    state_data = await state.get_data()
    story_link = state_data.get('link')

    requests_db.add_request(tg_id, login, offer_id, story_link, file_id)

    await state.finish()


@dp.callback_query_handler(lambda c: 'sale_btn' in c.data)
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    offer_id = int(callback_query.data.replace("sale_btn", ""))
    if offers_db.check_views_limit(offer_id) and not str(offer_id) in users_db.get_offers_taken(callback_query.from_user.id):
        users_db.add_offer(offer_id, callback_query.from_user.id)
        offers_db.increment_views(offer_id)
        await bot.send_message(callback_query.from_user.id, "Вы успешно заняли место")

        menu = get_two_btn_menu("Мои регистрации", "profile_btn" + str(offer_id), "Подробнее", "btn" + str(offer_id))

        await callback_query.message.edit_text("<b>" + callback_query.message.text + "</b>", reply_markup = menu, parse_mode = "HTML")

        """
            Переход на личные предложения
        """

    else:
        await bot.send_message(callback_query.from_user.id, "К сожалению, мест нет")
        """
            Кнопки для обновления
        """



    

    





if __name__ == '__main__':
    executor.start_polling(dp)