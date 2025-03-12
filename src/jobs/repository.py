"""Модуль для репозитория работы"""

from typing import Tuple

from sqlalchemy import Select, select

import src.jobs.schemas as schemas
from src.base.repository import BaseRepository
from src.jobs.models import Job


class JobRepository(
    BaseRepository[Job, schemas.JobCreateSchema, schemas.JobUpdateSchema]
):
    """Репозиторий работы"""

    model = Job

    @classmethod
    async def get_stmt_by_query(
        cls,
        query_params: schemas.JobPaginationSchema,
    ) -> Select[Tuple[Job]]:
        """
        Создать подготовленное выражение для запроса в БД,
        применив основные query параметры без учета пагинации,
        для получения списка пользователей.

        Args:
            query_params (JobPaginationSchema): параметры для запроса.

        Returns:
            stmt: Подготовленное выражение для запроса в БД.
        """

        stmt = select(Job)

        # Фильтрация
        if query_params.employer_address:
            stmt = stmt.where(
                Job.employer_address == query_params.employer_address,
            )

        if query_params.employee_address:
            stmt = stmt.where(
                Job.employee_address == query_params.employee_address,
            )

        return stmt
