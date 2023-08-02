from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import DuplicateDonateException
from app.api.validators import (check_charity_project_exists,
                                check_invested_amount, check_investing_funds,
                                check_name_duplicate, check_project_open)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models.donation import Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services import investing
from app.services.investing import close_obj, get_uninvested_objects, investing

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(charity_project, session)
    donations = await get_uninvested_objects(Donation, session)
    try:
        investing(
            opened_objects=donations, funds=new_charity_project
        )
        await session.commit()
        await session.refresh(new_charity_project)
    except IntegrityError:
        await session.rollback()
        raise DuplicateDonateException('Средства уже распределены')
    return new_charity_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projecs(
    session: AsyncSession = Depends(get_async_session)
):
    all_charity_projects = await charity_project_crud.get_multi(session)
    return all_charity_projects


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    await check_project_open(charity_project_id, session)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount:
        await check_investing_funds(charity_project_id, obj_in.full_amount, session)

    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    if obj_in.full_amount == charity_project.invested_amount:
        close_obj(charity_project)
        await session.commit()
        await session.refresh(charity_project)

    return charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
):

    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    await check_invested_amount(charity_project_id, session)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project
