from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Date, Numeric, Boolean
from decimal import Decimal
import datetime
from database import Base

class OneDayTourModel(Base):
    __tablename__ = "OneDayTour"

    id: Mapped[int] = mapped_column(primary_key=True)
    booking_id: Mapped[str] = mapped_column(unique=True, nullable=False)
    fio: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
    operator: Mapped[str] = mapped_column(nullable=False)
    direction: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    paydate: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    notified: Mapped[bool] = mapped_column(Boolean, default=False)


class LongTourModel(Base):
    __tablename__ = "LongTour"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    customer: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
    direction: Mapped[str] = mapped_column(nullable=False)
    p_count: Mapped[str] = mapped_column(nullable=False)
    bus: Mapped[str] = mapped_column(nullable=False)
    locations: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(scale=2, precision=12),nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)