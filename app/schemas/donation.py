from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.constants import DEFAULT_INVESTING_AMOUNT


class DonationBase(BaseModel):
    """Базовая схема пожертвований."""
    full_amount: PositiveInt = Field(..., title='Сумма пожертвования')
    comment: Optional[str] = Field(None, title='Комментарий к пожертвованию')

    class Config:
        title = 'Базовая схема пожертвования'


class DonationCreate(DonationBase):
    """Схема для создания пожертвования."""
    class Config:
        extra = Extra.forbid
        schema_extra = {
            'example': {
                'full_amount': 1000,
                'comment': 'QRKot'
            }
        }


class DonationDB(DonationBase):
    """Схема пожертвования для получения из базы пользователем."""
    id: int = Field(..., title='Идентификатор пожертвования')
    create_date: datetime = Field(..., title='Дата внесения пожертвования')

    class Config:
        title = 'Схема пожертвования для получения'
        orm_mode = True
        schema_extra = {
            'example': {
                'comment': 'QRKot',
                'full_amount': 500,
                'id': 2,
                'create_date': '2023-07-21T23:54:05.177Z'
            }
        }


class DonationDBSuper(DonationDB):
    """Схема пожертвования для получения из базы суперпользователем."""
    user_id: Optional[int] = Field(None, title='Идентификатор пользователя')
    invested_amount: int = Field(
        DEFAULT_INVESTING_AMOUNT,
        title='Сумма пожертвования',
    )
    fully_invested: bool = Field(False, title='Внесена полная сумма')
    close_date: Optional[datetime] = Field(None, title='Дата внесения пожертвования')

    class Config:
        title = 'Схема пожертвования для получения'
        orm_mode = True
        schema_extra = {
            'example': {
                'comment': 'QRKot',
                'full_amount': 500,
                'id': 2,
                'create_date': '2023-07-21T23:54:05.177Z',
                'user_id': 1,
                'invested_amount': 200,
                'fully_invested': 0
            }
        }
