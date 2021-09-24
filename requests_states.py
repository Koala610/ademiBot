from aiogram.dispatcher.filters.state import StatesGroup,State

class Req_states(StatesGroup):
	link = State()
	picture = State()