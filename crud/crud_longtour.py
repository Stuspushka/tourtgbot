from aiohttp.web_routedef import delete

from dbmodels import LongTourModel
from sqlalchemy import select, delete


async def create_long_tour(session, data: dict) -> LongTourModel:
    new_tour = LongTourModel(**data)
    session.add(new_tour)
    await session.commit()
    await session.refresh(new_tour)
    return new_tour


async def update_long_tour_by_name(session, name: str, field: str, value):
    result = await session.execute(
        select(LongTourModel).where(
            LongTourModel.name == name,
            LongTourModel.is_active == True
        )
    )
    tour = result.scalar_one_or_none()
    if not tour:
        return None
    setattr(tour, field, value)
    await session.commit()
    return tour


async def delete_long_tour(session, name: str) -> bool:
    result = await session.execute(
        delete(LongTourModel).where(LongTourModel.name == name)
    )
    await session.commit()
    return result.rowcount > 0


async def get_active_long_tours(session):
    result = await session.execute(
        select(LongTourModel)
        .where(LongTourModel.is_active == True)
        .order_by(LongTourModel.date.asc())
    )
    return result.scalars().all()