from sqlalchemy import select,delete
from dbmodels import OneDayTourModel


async def create_one_day_tour(session, data: dict):
    new_tour = OneDayTourModel(**data)
    session.add(new_tour)
    await session.commit()
    await session.refresh(new_tour)
    return new_tour


async def get_active_one_day_tours(session) -> list[OneDayTourModel]:
    result = await session.execute(
        select(OneDayTourModel)
        .where(OneDayTourModel.is_active == True)
        .order_by(OneDayTourModel.date.asc())
    )
    return result.scalars().all()


async def update_one_day_tour_by_booking_id(session, booking_id: str, field: str, value):
    result = await session.execute(
        select(OneDayTourModel).where(
            OneDayTourModel.booking_id == booking_id,
            OneDayTourModel.is_active == True
        )
    )
    tour = result.scalar_one_or_none()
    if not tour:
        return None
    setattr(tour, field, value)
    await session.commit()
    return tour


async def delete_one_day_tour(session, booking_id: str) -> bool:
    result = await session.execute(
        delete(OneDayTourModel).where(OneDayTourModel.booking_id == booking_id)
    )
    await session.commit()
    return result.rowcount > 0