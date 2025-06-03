from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboard import main_menu_keyboard, oneday_menu_keyboard, longtour_menu_keyboard

main_menu_router = Router()


@main_menu_router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Главное меню:", reply_markup=main_menu_keyboard)


@main_menu_router.message(F.text == "🗓 Однодневки")
async def show_oneday_menu(message: Message):
    await message.answer("Выберите действие с однодневками:", reply_markup=oneday_menu_keyboard)


@main_menu_router.message(F.text == "📆 Группы")
async def show_longtour_menu(message: Message):
    await message.answer("Выберите действие с группами:", reply_markup=longtour_menu_keyboard)


@main_menu_router.message(F.text == "🔙 Назад в меню")
async def back_to_main_menu(message: Message):
    await message.answer("Главное меню:", reply_markup=main_menu_keyboard)
