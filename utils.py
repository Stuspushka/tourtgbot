import asyncio
import logging
from datetime import date, timedelta
from settings import MAIN_ADMIN_ID
from database import Base, engine
from datetime import datetime
from decimal import Decimal
from aiogram import Bot
from sqlalchemy import select, update
from database import async_session
from dbmodels import OneDayTourModel, LongTourModel


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("bot.log", encoding='utf-8'),
            logging.StreamHandler(),
        ],
        force=True
    )
    logging.info("Логгирование успешно настроено")


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def is_valid_field(field: str) -> bool:
    valid_fields = {"fio", "phone", "direction", "date", "paydate"}
    return field in valid_fields


def parse_value(field: str, value: str):
    if field in {"date", "paydate"}:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    elif field == "total":
        return Decimal(value.strip())
    else:
        return value.strip()


async def notify_about_upcoming_paydates(bot: Bot):
    while True:
        try:
            async with async_session() as session:
                tomorrow = date.today() + timedelta(days=1)
                stmt = select(OneDayTourModel).where(
                    OneDayTourModel.is_active == True,
                    OneDayTourModel.paydate == tomorrow,
                    OneDayTourModel.notified == False
                )
                result = await session.execute(stmt)
                tours = result.scalars().all()

                for tour in tours:
                    text = (
                        f"🔔 Напоминание об оплате!\n"
                        f"Тур: {tour.direction} ({tour.date})\n"
                        f"ФИО: {tour.fio}\n"
                        f"📞 Тел: {tour.phone}\n"
                        f"💰 Оплата до: {tour.paydate}"
                    )
                    await bot.send_message(MAIN_ADMIN_ID, text)

                    stmt_update = (
                        update(OneDayTourModel)
                        .where(OneDayTourModel.id == tour.id)
                        .values(notified=True)
                    )
                    await session.execute(stmt_update)

                await session.commit()

        except Exception as e:
            logging.exception(f"Ошибка при уведомлении: {e}")

        await asyncio.sleep(3600 * 6)


async def deactivate_today_oneday_tours():
    while True:
        today = date.today()

        async with async_session() as session:
            result = await session.execute(
                select(OneDayTourModel).where(
                    OneDayTourModel.date == today,
                    OneDayTourModel.is_active == True
                )
            )
            tours_to_deactivate = result.scalars().all()

            if tours_to_deactivate:
                await session.execute(
                    update(OneDayTourModel)
                    .where(
                        OneDayTourModel.date <= today,
                        OneDayTourModel.is_active == True
                    )
                    .values(active=False)
                )
                await session.commit()
                logging.info(f"❌ Деактивировано {len(tours_to_deactivate)} однодневок за {today}")
            else:
                logging.info("⏳ Нет активных однодневок с датой на сегодня.")

        await asyncio.sleep(3600 * 6)


async def deactivate_today_longtours():
    while True:
        today = date.today()

        async with async_session() as session:
            result = await session.execute(
                select(LongTourModel).where(
                    LongTourModel.date == today,
                    LongTourModel.is_active == True
                )
            )
            tours_to_deactivate = result.scalars().all()

            if tours_to_deactivate:
                await session.execute(
                    update(LongTourModel)
                    .where(
                        LongTourModel.date <= today,
                        LongTourModel.is_active == True
                    )
                    .values(is_active=False)
                )
                await session.commit()
                logging.info(f"❌ Деактивировано {len(tours_to_deactivate)} групп за {today}")
            else:
                logging.info("⏳ Нет активных групп с датой на сегодня.")

        await asyncio.sleep(3600 * 6)
