from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from datetime import datetime
import re
from decimal import Decimal
from database import async_session
from crud.crud_longtour import create_long_tour, update_long_tour_by_name, delete_long_tour
from .models import AddLongTourState, EditLongTourState, DeleteLongTourState
from utils import parse_value
from keyboard import longtour_menu_keyboard, cancel_keyboard, confirm_longtour_delete_keyboard, \
    edit_longtour_fields_keyboard, main_menu_keyboard
from ..filters import NotCancelFilter

longtour_router = Router()


@longtour_router.message(F.text == "➕ Добавить группу")
async def start_add_longtour_button(message: Message, state: FSMContext):
    await state.set_state(AddLongTourState.name)
    await message.answer("Ок, начнём добавление тура. Введите название:", reply_markup=cancel_keyboard)


@longtour_router.message(F.text == "✏️ Редактировать группу")
async def start_edit_longtour_button(message: Message, state: FSMContext):
    await state.set_state(EditLongTourState.choosing_name)
    await message.answer("Введите уникальное имя тура (name) для редактирования:", reply_markup=cancel_keyboard)


@longtour_router.message(F.text == "🗑 Удалить группу")
async def start_delete_longtour_button(message: Message, state: FSMContext):
    await state.set_state(DeleteLongTourState.name)
    await message.answer("Введите название (name) тура, который нужно удалить:", reply_markup=cancel_keyboard)


@longtour_router.message(F.text, AddLongTourState.name, NotCancelFilter())
async def enter_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(AddLongTourState.customer)
    await message.answer("Введите ФИО заказчика:", reply_markup=cancel_keyboard)


@longtour_router.message(F.text, AddLongTourState.customer, NotCancelFilter())
async def enter_customer(message: Message, state: FSMContext):
    await state.update_data(customer=message.text.strip())
    await state.set_state(AddLongTourState.phone)
    await message.answer("Введите номер телефона:", reply_markup=cancel_keyboard)


@longtour_router.message(F.text, AddLongTourState.phone, NotCancelFilter())
async def enter_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    await state.set_state(AddLongTourState.direction)
    await message.answer("Введите направление:", reply_markup=cancel_keyboard)


@longtour_router.message(F.text, AddLongTourState.direction, NotCancelFilter())
async def enter_direction(message: Message, state: FSMContext):
    await state.update_data(direction=message.text.strip())
    await state.set_state(AddLongTourState.p_count)
    await message.answer("Введите количество человек (например, 5):", reply_markup=cancel_keyboard)


@longtour_router.message(F.text, AddLongTourState.p_count, NotCancelFilter())
async def enter_p_count(message: Message, state: FSMContext):
    await state.update_data(p_count=message.text.strip())
    await state.set_state(AddLongTourState.bus)
    await message.answer("Введите автобус:", reply_markup=cancel_keyboard)


@longtour_router.message(F.text, AddLongTourState.bus, NotCancelFilter())
async def enter_bus(message: Message, state: FSMContext):
    await state.update_data(bus=message.text.strip())
    await state.set_state(AddLongTourState.locations)
    await message.answer("Введите локации через запятую:", reply_markup=cancel_keyboard)


@longtour_router.message(F.text, AddLongTourState.locations, NotCancelFilter())
async def enter_locations(message: Message, state: FSMContext):
    raw_locations = re.split(r'[, \n]+', message.text)
    locations = [loc.strip() for loc in raw_locations if loc.strip()]
    if not locations:
        await message.answer("❌ Нужно ввести хотя бы одну локацию",
                             reply_markup=cancel_keyboard)
        return
    unique_locations = list(dict.fromkeys(locations))
    await state.update_data(locations=', '.join(unique_locations))
    await state.set_state(AddLongTourState.date)
    await message.answer("Теперь введите дату тура (ГГГГ-ММ-ДД):",
                         reply_markup=cancel_keyboard)


@longtour_router.message(F.text, AddLongTourState.date, NotCancelFilter())
async def enter_date(message: Message, state: FSMContext):
    try:
        date = datetime.strptime(message.text.strip(), "%Y-%m-%d").date()
    except ValueError:
        await message.answer("Неверный формат даты. Используйте ГГГГ-ММ-ДД. Попробуйте снова:",
                             reply_markup=cancel_keyboard)
        return
    await state.update_data(date=date)
    await state.set_state(AddLongTourState.total)
    await message.answer("Введите общую сумму (total):", reply_markup=cancel_keyboard)


@longtour_router.message(F.text, AddLongTourState.total, NotCancelFilter())
async def enter_total(message: Message, state: FSMContext):
    try:
        total = Decimal(message.text.strip())
    except Exception:
        await message.answer("Сумма должна быть числом. Попробуйте снова:", reply_markup=cancel_keyboard)
        return
    await state.update_data(total=total)
    data = await state.get_data()
    async with async_session() as session:
        try:
            new_tour = await create_long_tour(session, data)
            await message.answer(f"✅ Группа добавлена! ID: {new_tour.id}", reply_markup=longtour_menu_keyboard)
        except Exception as e:
            await message.answer(f"Ошибка при добавлении тура: {e}", reply_markup=longtour_menu_keyboard)

    await state.clear()


@longtour_router.message(DeleteLongTourState.name, NotCancelFilter())
async def ask_delete_confirmation(message: Message, state: FSMContext):
    name = message.text.strip()
    await state.update_data(name=name)
    await message.answer(
        f"Вы уверены, что хотите удалить тур с названием: *{name}*?",
        parse_mode="Markdown",
        reply_markup=confirm_longtour_delete_keyboard
    )


@longtour_router.message(EditLongTourState.choosing_name, F.text)
async def show_edit_keyboard(message: Message, state: FSMContext):
    name = message.text.strip()
    await state.update_data(name=name)
    await message.answer(
        "Выберите поле для редактирования:",
        reply_markup=edit_longtour_fields_keyboard(name)
    )
    await state.set_state(EditLongTourState.choosing_field)


@longtour_router.callback_query(F.data.startswith("edit_longtour:"))
async def handle_longtour_field_selection(callback: CallbackQuery, state: FSMContext):
    _, field, name = callback.data.split(":", 2)
    await state.update_data(field=field, name=name)
    await callback.message.edit_text(f"Введите новое значение для поля: *{field}*")
    await callback.answer()
    await state.set_state(EditLongTourState.entering_value)


@longtour_router.message(EditLongTourState.entering_value, F.text)
async def apply_longtour_edit(message: Message, state: FSMContext):
    data = await state.get_data()
    field = data["field"]
    name = data["name"]

    try:
        new_value = parse_value(field, message.text)
    except Exception:
        await message.answer("❌ Неверный формат. Для даты используйте ГГГГ-ММ-ДД, для суммы — число.")
        return

    async with async_session() as session:
        result = await update_long_tour_by_name(session, name, field, new_value)

    if result:
        await message.answer(f"✅ Поле *{field}* успешно обновлено.", reply_markup=longtour_menu_keyboard)
    else:
        await message.answer("❌ Не удалось обновить. Тур не найден или ошибка базы данных.",
                             reply_markup=longtour_menu_keyboard)

    await state.clear()


@longtour_router.callback_query(F.data == "cancel_longtour_edit")
async def cancel_longtour_edit(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("❌ Редактирование отменено.", reply_markup=longtour_menu_keyboard)
    await callback.answer()
    await state.clear()


@longtour_router.callback_query(F.data == "confirm_delete")
async def confirm_delete_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")

    async with async_session() as session:
        success = await delete_long_tour(session, name)

    if success:
        await callback.message.answer(f"✅ Тур с названием '{name}' успешно удалён.",
                                      reply_markup=longtour_menu_keyboard)
    else:
        await callback.message.answer("❌ Тур не найден или уже удалён.", reply_markup=longtour_menu_keyboard)

    await callback.answer()
    await state.clear()


@longtour_router.callback_query(F.data == "cancel_delete")
async def cancel_delete_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Удаление отменено.", reply_markup=longtour_menu_keyboard)
    await callback.answer()
    await state.clear()
