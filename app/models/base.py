from datetime import datetime
# импортируем базовый класс, на основе которого создаем нашу модель
# основу для моделей donation и charity_project
# т.к у них часть полей одинаковые, и принцип DRY требует вынести
# их в отдельный родительский класс
from app.core.db import Base
from sqlalchemy import Column, CheckConstraint, Integer, Boolean, DateTime
from app.constants import DEFAULT_INVESTING_AMOUNT


# создаем родительский абстрактный класс для моделей проектов и пожертвований
# используем метод __abstract__, чтобы сделать ее абстрактной
# - т.е для этой модели не должна создаваться таблица в БД
class InvestBaseModel(Base):
    __abstract__ = True
    # добавим аттрибут __table_args__, который предназначен для работы с полями
    # в таблице БД, например для проверки полей
    __table_args__ = (
        # что сумма пожертвований больше 0
        CheckConstraint('full_amount > 0'),
        # что сумма пожертвований меньше требуемой суммы сбора
        CheckConstraint('invested_amount < full_amount'),
        # что сумма пожертвований больше нуля
        CheckConstraint('invested_amount >= 0')
    )
    """Базовый абстрактный класс для моделей проектов и пожертвований."""
    # здесь укажем общие поля для моделей проекты и пожертвования
    # поле full_amount - требуемая сумма сбора
    # целочисленное значение, больше 0
    full_amount = Column(Integer, nullable=False)
    # внесенная сумма, целочисленное поле,
    # значение по умолчанию 0
    invested_amount = Column(Integer, default=DEFAULT_INVESTING_AMOUNT)
    # поле fully_invested - булево значение
    # указывает на то, собрана ли нужная сумма для проекта
    # по умолчанию False
    fully_invested = Column(Boolean, default=False)
    # поле create_date - дата создания проекта,
    # можно добавлять автоматически в момент создания проекта
    create_date = Column(DateTime, default=datetime.utcnow())
    # поле close_date - дата закрытия проекта, DateTime,
    # проставляется автоматически в момент набора нужной суммы
    close_date = Column(DateTime)
