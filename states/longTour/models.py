from aiogram.fsm.state import StatesGroup, State


class AddLongTourState(StatesGroup):
    name = State()
    customer = State()
    phone = State()
    direction = State()
    p_count = State()
    bus = State()
    locations = State()
    date = State()
    total = State()


class EditLongTourState(StatesGroup):
    choosing_name = State()
    choosing_field = State()
    entering_value = State()

class DeleteLongTourState(StatesGroup):
    name = State()