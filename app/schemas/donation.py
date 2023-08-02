from datetime import datetime
from pydantic import BaseModel, PositiveInt
from typing import Optional


# создаем базовую схему, которая будет содержать повторяющиеся аттрибуты
# а далее от нее нследуем схемы DonationCreate и DonationRead
# тем самым соблюдаем принцип DRY
# избегаем повторяющегося кода
class DonationBase(BaseModel):
    """Базовая схема."""
    # типы аттрибутов устанавливаем в соответствии с ограничениями по ТЗ
    # full_amount(требуемая сумма сбора) должна быть строго больше 0
    # поэтому указываем PositiveInt
    # сomment - необязательное текстовое поле,
    #  поэтому укажем Optional[str]
    full_amount: PositiveInt
    comment: Optional[str]

    # добавляем подкласс Config и в нем через аттрибут schema_extra
    # укажем примеры запросов
    class Config:
        schema_extra = {
            'example': {
                'full_amount': 1000,
                'comment': 'QRKot'
            }
        }


# схема для создания пожертвования
# она содержит только те аттрибуты, которые есть у базовой схемы
# так что расширять базовую схему не потребуется
# также не добавляем и подкласс Config c примером запроса
# так как он наследуется полностью от базовой схемы
class DonationCreate(DonationBase):
    """Схема для создания пожертвования."""
    pass


# схема для получения пожертвований пользователя, сделавшего запрос
class DonationRead(DonationBase):
    """
    Схема для получения всех пожертвований пользователя, сделавшего запрос.
    """
    id: int
    user_id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_time: Optional[datetime]

    # добавляем подкласс Config с аттрибутом schema_extra
    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'full_amount': 1000,
                'comment': 'QRKot',
                'id': 1,
                'create_date': "2019-08-24T14:15:22Z"
            }
        }


# # схема для получения списка всех пожертвований
# # наследуем от схемы DonationRead, так как она включает в себя
# # аттрибуты базовой схемы, а также два дполонительных аттрибута
# # которые также должны быть и у текущей схемы
# # соблюдение принципа DRY
# class DonationReadAll(DonationRead):
#     """Схема для получения всех пожертвований."""
#     user_id: int
#     invested_amount: NonNegativeInt
#     fully_invested: bool
#     close_date: datetime

#     # добавляем подкласс Config c аттрибутом schema_extra
#     # который позволяет добавить пример запроса
#     class Config:
#         schema_extra = {
#             'example': {
#                 'full_amount': 1000,
#                 'comment': 'QRKot',
#                 'id': 1,
#                 'create_date': "2019-08-24T14:15:22Z",
#                 'user_id': 1,
#                 'invested_amount': 10000,
#                 'fully_invested': True,
#                 'close_date': "2019-08-24T14:15:22Z"
#             }
#         }
