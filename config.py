from aiogram import Bot, Dispatcher
from settings import API_TOKEN
from commands.oneday import oneday_command_router
from commands.longtour import longtour_command_router
from states.oneday.states import oneday_router
from states.longTour.states import longtour_router
from menu import main_menu_router


bot = Bot(token=API_TOKEN)
dp = Dispatcher()

dp.include_router(main_menu_router)
dp.include_router(oneday_command_router)
dp.include_router(longtour_command_router)
dp.include_router(oneday_router)
dp.include_router(longtour_router)
