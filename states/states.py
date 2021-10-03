from aiogram.dispatcher.filters.state import StatesGroup,State

class States(StatesGroup):
	login = State()
	password = State()
	main_menu = State()
	name = State()
	surname = State()
	gender = State()
	date = State()
	end = State()