from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    """Расширенный CRUD-класс для проектов пожертвований."""

    async def get_charity_project_id_by_name(
        self,
        charity_project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        """Поиск id проекта по названию."""
        charity_project_id = await session.execute(
            select(
                CharityProject.id
            ).where(
                CharityProject.name == charity_project_name
            )
        )
        return charity_project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self, session: AsyncSession) -> List:
        """
        Метод, который отсортирует список со всеми
        закрытыми проектами пожертвований.
        """
        # отбираем проекты, у которых fully_invested = True
        # т.е проекты, у которых сбор закрыт
        close_projects = await session.execute(
            select(
                CharityProject.name,
                CharityProject.close_date,
                CharityProject.description).where(
                    CharityProject.fully_invested))
        # создаем пустой список
        result = []
        # и далее этот список наполняем уже отсортированными по показателю интервал
        # закрытыми проектами
        for project in close_projects:
            result.append({
                'name': project.name,
                'interval': project.close_date - project.create_date,
                'description': project.description})
        # используем функцию sorted(), которая возвращает новый отсортированный список
        # итерируемого объекта(списка result)
        # сортировать можно по функции, указанной в параметре key
        # первым параметром передаем итерируемый объект
        # вторым параметром передаем key. И в key мы должны указать функцию
        # которая будет учитывать скорость сбора средств - то есть, interval
        #разницу между закрытием и открытием сбора
        return sorted(result, key=lambda x: x['interval'])


charity_project_crud = CRUDCharityProject(CharityProject)
