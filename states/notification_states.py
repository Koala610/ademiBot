from aiogram.dispatcher.filters.state import StatesGroup,State

class Notification_states(StatesGroup):
	message_state = State()
	id_obtain = State()