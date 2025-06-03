import os
from dotenv import load_dotenv
import logging


load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USERS = set(map(int, os.getenv("ALLOWED_USERS", "").split(",")))
MAIN_ADMIN_ID = os.getenv("MAIN_ADMIN_ID")


if not API_TOKEN:
    logging.error("Ошибка: TELEGRAM_BOT_TOKEN не задан в переменных окружения!")
else:
    logging.info("Токен успешно загружен.")