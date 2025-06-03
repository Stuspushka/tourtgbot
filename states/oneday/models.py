from aiogram.fsm.state import State, StatesGroup

class EditOneDayTourState(StatesGroup):
    choosing_id = State()
    choosing_field = State()
    entering_value = State()


class AddOneDayTourState(StatesGroup):
    booking_id = State()
    fio = State()
    phone = State()
    operator = State()
    direction = State()
    date = State()
    paydate = State()

class DeleteOneDayTourState(StatesGroup):
    booking_id = State()