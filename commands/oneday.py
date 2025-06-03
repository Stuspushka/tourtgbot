from aiogram import Router, F
from aiogram.types import Message
from database import async_session
from crud.crud_oneday import get_active_one_day_tours
from keyboard import oneday_menu_keyboard

oneday_command_router = Router()


@oneday_command_router.message(F.text == "📋 Показать однодневки")
async def list_one_day_tours_handler(message: Message):
    async with async_session() as session:
        tours = await get_active_one_day_tours(session)

    if not tours:
        await message.answer("Нет активных однодневных туров.")
        return

    response = "📋 Список однодневных туров:\n\n"
    for tour in tours:
        response += (
            f"🆔 {tour.id} | {tour.booking_id}\n"
            f"👤 {tour.fio} 📞 {tour.phone}\n"
            f"📍 {tour.direction} 🚌 {tour.operator}\n"
            f"📅 Тур: {tour.date} | Оплата до: {tour.paydate}\n\n"
        )

    await message.answer(response[:4096], reply_markup=oneday_menu_keyboard)
