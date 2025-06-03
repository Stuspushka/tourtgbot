from aiogram import Router, F
from aiogram.types import Message
from database import async_session
from crud.crud_longtour import get_active_long_tours
from keyboard import longtour_menu_keyboard

longtour_command_router = Router()


@longtour_command_router.message(F.text == "📋 Показать группы")
async def show_long_tours_handler(message: Message):
    async with async_session() as session:
        tours = await get_active_long_tours(session)

    if not tours:
        await message.answer("Нет активных групп.")
        return

    response = "📋 Список групп:\n\n"
    for tour in tours:
        response += (
            f"🆔 {tour.id} | {tour.name}\n"
            f"👤 {tour.customer} 📞 {tour.phone}\n"
            f"📍 {tour.direction} 🚌 {tour.bus} 👥 {tour.p_count}\n"
            f"🗺️ Локации: {tour.locations}\n"
            f"📅 Дата: {tour.date} 💵 Сумма: {tour.total}₽\n\n"
        )

    await message.answer(response[:4096], reply_markup=longtour_menu_keyboard)
