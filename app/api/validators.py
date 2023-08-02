from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_projects import charity_project_crud
from app.models import CharityProject


# код проверки вынесем в отдельную корутину в  файле валидаторов
async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """
    Валидатор, который проверяет, что объект проекта пожертвований содержится в базе данных.
    """
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charity_project


# еще одну проверку вынесем в отдельную корутину-валидатор
async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """
    Валидатор, который проверяет, существует ли проект с указанным именем.
    """
    project_id = await charity_project_crud.get_charity_project_id_by_name(
        project_name, session)
    if project_id:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!',
        )
