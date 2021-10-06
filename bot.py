from command_proccessing_functions import *


@dp.message_handler()
async def bot_message(message: types.Message):
    if users_db.tg_id_exists(message.from_user.id):
        try:
            await command_switch[message.text](message)
        except KeyError:
            return -1
    else:
        await bot.send_message(message.from_user.id, "Вы не авторизованны...", reply_markup=login_menu)











if __name__ == '__main__':
    executor.start_polling(dp)
