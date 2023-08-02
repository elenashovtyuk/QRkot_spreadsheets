from datetime import datetime
from typing import List, Optional, Type, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation

ComplexTypeObjects = Union[Donation, CharityProject]


# функция процесса инвестирования
def investing(
        opened_objects: Optional[List[ComplexTypeObjects]],
        funds: ComplexTypeObjects,
) -> ComplexTypeObjects:
    if opened_objects:
        for item in opened_objects:
            funds_diff = funds.full_amount - funds.invested_amount
            item_diff = item.full_amount - item.invested_amount
            if funds_diff >= item_diff:
                funds.invested_amount += item_diff
                item.invested_amount = item.full_amount
                close_obj(item)
                if funds_diff == item_diff:
                    close_obj(funds)
            else:
                item.invested_amount += funds_diff
                funds.invested_amount = funds.full_amount
                close_obj(funds)
                break
    return funds


def close_obj(item: ComplexTypeObjects) -> ComplexTypeObjects:
    item.fully_invested = True
    item.close_date = datetime.now()
    return item


async def get_uninvested_objects(
        obj_model: Type[ComplexTypeObjects],
        session: AsyncSession,
) -> Optional[List[ComplexTypeObjects]]:
    uninvested_objects = await session.execute(
        select(obj_model).where(
            obj_model.fully_invested == 0
        ).order_by(obj_model.create_date)
    )
    return uninvested_objects.scalars().all()
