from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.constants import DEFAULT_INVESTING_AMOUNT, MAX_LENGTH, MIN_LENGTH


class CharityProjectBase(BaseModel):
    """Базовая схема проекта."""
    name: Optional[str] = Field(
        None,
        title='Название',
        min_length=MIN_LENGTH,
        max_length=MAX_LENGTH,
    )
    description: Optional[str] = Field(None, title='Описание')
    full_amount: Optional[PositiveInt] = Field(None, title='Требуемая сумма')

    class Config:
        title = 'Базовая схема проекта'


class CharityProjectUpdate(CharityProjectBase):
    """
    Схема для обновления (полного или частичного)
    существующего проекта пожертвований.
    """
    class Config:
        title = 'Схема проекта для обновления'
        orm_mode = True
        extra = Extra.forbid
        schema_extra = {
            'example': {
                'name': 'Сбор на лекарства котикам',
                'description': 'Чтобы все котики были здоровы',
                'full_amount': 1000
            }
        }

    @validator('name')
    def name_cannot_be_null(cls, value: str):
        if not value:
            raise ValueError('Название проекта не может оставаться пустым!')
        return value

    @validator('description')
    def description_cannot_be_null(cls, value: str):
        if not value:
            raise ValueError('Описание проекта не может оставаться пустым!')
        return value


class CharityProjectCreate(CharityProjectUpdate):
    """Схема для создания проекта."""
    name: str = Field(
        ...,
        title='Название',
        min_length=MIN_LENGTH,
        max_length=MAX_LENGTH,
    )
    description: str = Field(..., title='Описание')
    full_amount: PositiveInt = Field(..., title='Требуемая сумма')

    class Config:
        title = 'Схема для создания проекта'
        extra = Extra.forbid


class CharityProjectDB(CharityProjectCreate):
    """Схема для получения проекта."""
    id: int = Field(
        ...,
        title='Порядковый номер'
    )
    invested_amount: int = Field(
        DEFAULT_INVESTING_AMOUNT,
        title='Сумма пожертвования'
    )
    fully_invested: bool = Field(
        False,
        title='Собрана нужная для закрытия сумма')
    create_date: datetime = Field(
        ...,
        title='Дата открытия проекта пожертвования'
    )
    close_date: Optional[datetime] = Field(
        None,
        title='Дата закрытия проекта')

    class Config:
        title = 'Схема для получения проекта пожертвования'
        orm_mode = True
        schema_extra = {
            'example': {
                'name': 'Котики - наши друзья',
                'description': 'Поможем котикам вместе',
                'full_amoun': 5000,
                'id': 10,
                'invested_amount': 300,
                'fully_invested': 0,
                'create_date': '2023-07-22T02:18:40.662286'
            }
        }
