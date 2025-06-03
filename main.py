import asyncio
import logging
from utils import setup_logging

setup_logging()

from config import bot, dp
from filters import AccessMiddleware
from utils import create_tables, notify_about_upcoming_paydates, deactivate_today_oneday_tours, deactivate_today_longtours

dp.message.middleware(AccessMiddleware())
dp.callback_query.middleware(AccessMiddleware())

async def main():
    logging.info("Начало создания таблиц...")
    await create_tables()
    logging.info("Таблицы созданы, запуск бота...")
    try:
        await asyncio.gather(
            dp.start_polling(bot),
            deactivate_today_oneday_tours(),
            deactivate_today_longtours(),
            notify_about_upcoming_paydates(bot)
        )
    except Exception as e:
        logging.exception(f"Ошибка: {e}")
    finally:
        logging.info("Закрытие сессии...")
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
