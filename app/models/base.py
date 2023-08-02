from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.constants import DEFAULT_INVESTING_AMOUNT
from app.core.db import Base


class InvestBaseModel(Base):
    """
    Абстрактный базовая модель для моделей
    проектов и пожертвований.
    """
    __abstract__ = True
    __table_args__ = (
        CheckConstraint('full_amount > 0'),
        CheckConstraint('invested_amount <= full_amount'),
        CheckConstraint('invested_amount >= 0')
    )
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(
        Integer,
        nullable=False,
        default=DEFAULT_INVESTING_AMOUNT
    )
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now)
    close_date = Column(DateTime)
