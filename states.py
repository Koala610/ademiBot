from aiogram.dispatcher.filters.state import StatesGroup,State

class States(StatesGroup):
	login = State()
	password = State()