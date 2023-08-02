# импортируем базовый CRUD-класс, чтобы для модели Donation
# можно было использовать CRUD-методы базового класса
from app.crud.base import CRUDBase
from typing import List
# импортируем модель Donation
from app.models import Donation, User
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


# наследуем класс от базового CRUDBase-класса
# который включает в себя основные круд-функции
# а также расширяем его, добавляем уникальную корутину
# которая возвращает все пожертвования пользователя, выполнившего запрос
class CRUDDonation(CRUDBase):
    async def get_user_donations(
        self,
        session: AsyncSession,
        user: User
    ) -> List[Optional[Donation]]:
        reservations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return reservations.scalars().all()


donation_crud = CRUDDonation(Donation)
