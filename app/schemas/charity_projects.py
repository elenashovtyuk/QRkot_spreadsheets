# создадим отдельные Pydantic-схемы для разных эндпоинтов
# так как для разных эндпоинтов разные поля являются обязательными или опциональными
# чтобы легче было ориентироваться в названии схемы будем указывать
# ее назначение
from datetime import datetime
from pydantic import BaseModel, Field, PositiveInt
from typing import Optional


# схема для создания проекта пожертвований
# доп.свойства полей прописываем с помощью класса Field

class CharityProjectCreate(BaseModel):
    """Схема для создания нового проекта пожертвований."""
    name: str = Field(..., max_length=100)
    description: str
    full_amount: PositiveInt

    class Config:
        schema_extra = {
            'example': {
                'name': 'QRKot',
                'description': 'На вкусняшки котикам',
                'full_amount': 2500,
            }
        }
        min_anystr_length = 1


# создаем схему для обновления проекта пожертвований
# так как обновлять можем каждое поле отдельно и все сразу, то
#
class CharityProjectUpdate(BaseModel):
    """
    Схема для изменения (полного или частичного)
    существующего проекта пожертвований.
    """
    name: Optional[str] = Field(..., max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        min_anystr_length = 1


# создаем схему, которая описывает объект
# проекта пожертвований, полученный из БД
# наследуем ее от схемы для создания нового проекта, чтобы не дублировать
# код с повторяющимися полями(name, description, fuul_amount)
class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
