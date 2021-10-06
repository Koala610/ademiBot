from callback_views import *
from state_views import *



async def add_message_to_dl(message_id, user_id):
    strg = await dp.storage.get_data(user = user_id)
    message_list = strg.get('msg_list')
    message_list.append(message_id)
    await dp.storage.update_data(msg_list = message_list, user = user_id)



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
