from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    """Расширенный CRUD-класс для пожертвований."""
    async def get_user_donations(
        self,
        session: AsyncSession,
        user: User
    ) -> Optional[List[Donation]]:
        """Поиск пожертвования по его id."""
        reservations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return reservations.scalars().all()


donation_crud = CRUDDonation(Donation)
