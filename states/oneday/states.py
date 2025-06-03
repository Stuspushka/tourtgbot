from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from utils import parse_value
from database import async_session
from crud.crud_oneday import update_one_day_tour_by_booking_id, create_one_day_tour, delete_one_day_tour
from datetime import datetime
from .models import AddOneDayTourState, EditOneDayTourState, DeleteOneDayTourState
from keyboard import (oneday_menu_keyboard, confirm_oneday_delete_keyboard, cancel_keyboard, edit_oneday_fields_keyboard,
                      main_menu_keyboard)
from ..filters import NotCancelFilter

oneday_router = Router()


@oneday_router.message(Command("cancel"))
@oneday_router.message(F.text == "❌ Отмена")
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Нет активного действия для отмены.", reply_markup=main_menu_keyboard)
        return
    await message.answer("Действие отменено", reply_markup=main_menu_keyboard)
    await state.clear()


@oneday_router.message(F.text == "➕ Добавить однодневку")
async def start_add_from_button(message: Message, state: FSMContext):
    await message.answer("Ок, начнём добавление тура. Введите booking_id:", reply_markup=cancel_keyboard)
    await state.set_state(AddOneDayTourState.booking_id)


@oneday_router.message(F.text == "✏️ Обновить однодневку")
async def start_edit_from_button(message: Message, state: FSMContext):
    await message.answer("Введите Booking ID записи для редактирования:", reply_markup=cancel_keyboard)
    await state.set_state(EditOneDayTourState.choosing_id)


@oneday_router.message(F.text == "🗑 Удалить однодневку")
async def start_delete_from_button(message: Message, state: FSMContext):
    await state.set_state(DeleteOneDayTourState.booking_id)
    await message.answer("Введите id (booking_id) тура, который нужно удалить:", reply_markup=cancel_keyboard)


@oneday_router.message(AddOneDayTourState.booking_id, F.text, NotCancelFilter())
async def get_booking_id(message: Message, state: FSMContext):
    await state.update_data(booking_id=message.text.strip())
    await state.set_state(AddOneDayTourState.fio)
    await message.answer("Введите ФИО:", reply_markup=cancel_keyboard)


@oneday_router.message(AddOneDayTourState.fio, F.text, NotCancelFilter())
async def get_fio(message: Message, state: FSMContext):
    await state.update_data(fio=message.text.strip())
    await state.set_state(AddOneDayTourState.phone)
    await message.answer("Введите номер телефона:", reply_markup=cancel_keyboard)


@oneday_router.message(AddOneDayTourState.phone, F.text, NotCancelFilter())
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    await state.set_state(AddOneDayTourState.operator)
    await message.answer("Введите оператора:", reply_markup=cancel_keyboard)


@oneday_router.message(AddOneDayTourState.operator, F.text, NotCancelFilter())
async def get_operator(message: Message, state: FSMContext):
    await state.update_data(operator=message.text.strip())
    await state.set_state(AddOneDayTourState.direction)
    await message.answer("Введите направление:", reply_markup=cancel_keyboard)


@oneday_router.message(AddOneDayTourState.direction, F.text, NotCancelFilter())
async def get_direction(message: Message, state: FSMContext):
    await state.update_data(direction=message.text.strip())
    await state.set_state(AddOneDayTourState.date)
    await message.answer("Введите дату тура (ГГГГ-ММ-ДД):", reply_markup=cancel_keyboard)


@oneday_router.message(AddOneDayTourState.date, F.text, NotCancelFilter())
async def get_date(message: Message, state: FSMContext):
    try:
        date = datetime.strptime(message.text.strip(), "%Y-%m-%d").date()
    except ValueError:
        await message.answer("Неверный формат даты. Используйте ГГГГ-ММ-ДД:", reply_markup=cancel_keyboard)
        return
    await state.update_data(date=date)
    await state.set_state(AddOneDayTourState.paydate)
    await message.answer("Введите дату доплаты (ГГГГ-ММ-ДД):", reply_markup=cancel_keyboard)


@oneday_router.message(AddOneDayTourState.paydate, F.text, NotCancelFilter())
async def get_paydate_and_save(message: Message, state: FSMContext):
    try:
        paydate = datetime.strptime(message.text.strip(), "%Y-%m-%d").date()
    except ValueError:
        await message.answer("Неверный формат даты. Используйте ГГГГ-ММ-ДД:", reply_markup=cancel_keyboard)
        return
    await state.update_data(paydate=paydate)
    data = await state.get_data()
    date = data.get("date")
    if date and paydate > date:
        await message.answer("Дата доплаты не может быть позже даты тура. Попробуйте снова.",
                             reply_markup=cancel_keyboard)
        return
    async with async_session() as session:
        try:
            new_tour = await create_one_day_tour(session, data)
            await message.answer(f"✅ Тур добавлен! ID: {new_tour.id}", reply_markup=oneday_menu_keyboard)
        except Exception as e:
            await message.answer(f"Ошибка при добавлении: {e}", reply_markup=oneday_menu_keyboard)
    await state.clear()


@oneday_router.message(EditOneDayTourState.choosing_id, F.text)
async def choose_field(message: Message, state: FSMContext):
    booking_id = message.text.strip()
    await state.update_data(booking_id=booking_id)

    keyboard = edit_oneday_fields_keyboard(booking_id)
    await message.answer(
        text=f"Выберите поле для редактирования тура с booking_id `{booking_id}`:",
        reply_markup=keyboard
    )

    await state.set_state(EditOneDayTourState.choosing_field)


@oneday_router.callback_query(F.data.startswith("edit_oneday"))
async def handle_edit_callback(callback: CallbackQuery, state: FSMContext):
    _, field, booking_id = callback.data.split(":", 2)

    await state.update_data(field=field, booking_id=booking_id)
    await callback.message.answer(f"Введите новое значение для поля *{field}*:")

    await state.set_state(EditOneDayTourState.entering_value)
    await callback.answer()


@oneday_router.callback_query(F.data == "cancel_edit")
async def cancel_edit_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Редактирование отменено.", reply_markup=oneday_menu_keyboard)
    await state.clear()
    await callback.answer()


@oneday_router.message(EditOneDayTourState.entering_value, F.text)
async def apply_edit(message: Message, state: FSMContext):
    data = await state.get_data()
    field = data["field"]
    booking_id = data["booking_id"]

    try:
        new_value = parse_value(field, message.text)
    except Exception:
        await message.answer("❗ Неверный формат. Для дат — ГГГГ-ММ-ДД.")
        return

    async with async_session() as session:
        tour = await update_one_day_tour_by_booking_id(session, booking_id, field, new_value)
        if not tour:
            await message.answer("❌ Запись с таким Booking ID не найдена.", reply_markup=oneday_menu_keyboard)
        else:
            await message.answer(f"✅ Поле `{field}` обновлено.", reply_markup=oneday_menu_keyboard)

    await state.clear()


@oneday_router.message(DeleteOneDayTourState.booking_id, NotCancelFilter())
async def ask_oneday_delete_confirmation(message: Message, state: FSMContext):
    booking_id = message.text.strip()
    await state.update_data(booking_id=booking_id)
    await message.answer(
        f"Вы точно хотите удалить однодневный тур под номером *{booking_id}*?",
        reply_markup=confirm_oneday_delete_keyboard
    )


@oneday_router.callback_query(F.data == "confirm_oneday_delete")
async def confirm_oneday_delete(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    booking_id = data.get("booking_id")

    async with async_session() as session:
        success = await delete_one_day_tour(session, booking_id)

    if success:
        await callback.message.answer(f"✅ Тур '{booking_id}' успешно удалён.", reply_markup=oneday_menu_keyboard)
    else:
        await callback.message.answer("❌ Тур не найден или уже удалён.", reply_markup=oneday_menu_keyboard)

    await state.clear()
    await callback.answer()


@oneday_router.callback_query(F.data == "cancel_oneday_delete")
async def cancel_oneday_delete(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Удаление отменено.", reply_markup=oneday_menu_keyboard)
    await state.clear()
    await callback.answer()
