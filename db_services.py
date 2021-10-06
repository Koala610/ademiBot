from settings import *

async def add_message_to_dl(message_id, user_id):
    strg = await dp.storage.get_data(user = user_id)
    message_list = strg.get('msg_list')
    message_list.append(message_id)
    await dp.storage.update_data(msg_list = message_list, user = user_id)


def get_requests_by_status(status, user_id):
    if status == None:
        return requests_db.get_all_requests()
    else:
        return [requests_db.get_users_requests_by_status(user_id, status)]


def check_if_offer_exist(offer_id):
    try:
        is_exist = int(offer_id) in offers_db.get_all_ids()
    except ValueError:
        return False
    return is_exist

def get_offers_taken(src):
    offers_list = users_db.get_offers_taken(src.from_user.id)
    return offers_list


def _check_if_offer_valid(user_id, cur_date, offer) -> bool:
    is_in_time_range = cur_date <= offer[3] and cur_date >= offer[2]
    is_in_users_offers = str(offer[0]) in users_db.get_offers_taken(user_id)
    is_in_requests = requests_db.check_if_users_offer_exists(user_id, offer[0])
    return is_in_time_range and not is_in_users_offers and not is_in_requests

def check_if_cur_offers_exist(category_id, user_id):
    offers = offers_db.get_offers(category_id)
    for offer in offers:
        if _check_if_offer_valid(
            user_id, datetime.datetime.now().date(), offer):
                return True
    return False


def get_cur_offers(src, category_id):
    user_id = src.from_user.id
    offers = offers_db.get_offers(category_id)
    cur_offers = [offer for offer in offers if offers_db.check_views_limit(offer[0]) and
                  _check_if_offer_valid(user_id, datetime.datetime.now().date(),
                  offer)]
    return cur_offers

def get_categories_markup_menu(user_id):
    menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for category in CATEGORIES:
        if check_if_cur_offers_exist(category_id=CATEGORIES[category]['id'], user_id = user_id):
            menu.add(KeyboardButton(category))
    return menu

def get_business_name(offer):
	return offers_db.get_business_name(offers_db.get_business_id(offer))


def get_offers_info(user_id, msg_id, offer, inl_btn):
    bus_name = get_business_name(offer)
    btn_callback_data2 = "more_btn::" + str(offer) + "::" + msg_id + "::" + str(user_id) +inl_btn[2]
    menu = get_two_btn_menu(inl_btn[0], inl_btn[1] + str(offer), "Подробнее", btn_callback_data2)
    result = "<b>Заведение: %s </b>"%(bus_name) + "\n"
    result += "<b>ID заказа: %s </b>"%(offer)
    return result, menu