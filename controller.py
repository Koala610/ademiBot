from callback_views import *
from state_views import *
from views import *

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


@dp.message_handler()
async def bot_message(message: types.Message):
    if users_db.tg_id_exists(message.from_user.id) and \
       not users_db.check_if_new(message.from_user.id):
        try:
            await command_switch[message.text](message)
        except KeyError:
            return -1
    else:
        await bot.send_message(message.from_user.id, "Вы не авторизованны...", reply_markup=login_menu)




