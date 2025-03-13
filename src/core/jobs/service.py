"""Модуль для сервиса работы"""

from sqlalchemy.ext.asyncio import AsyncSession

import src.core.base.schemas as base_schemas
import src.core.jobs.schemas as schemas
from src.core import exceptions
from src.core.base import BaseService
from src.core.jobs.models import Job
from src.core.jobs.repository import JobRepository


class JobService(
    BaseService[
        Job,
        schemas.JobCreateSchema,
        schemas.JobGetSchema,
        base_schemas.PaginationBaseSchema,
        schemas.JobListGetSchema,
        schemas.JobUpdateSchema,
    ]
):
    """Сервис работы"""

    repository = JobRepository()

    # MARK: Create
    @classmethod
    async def create_application(
        cls,
        session: AsyncSession,
        data: schemas.JobApplicationSchema,
    ):
        """
        Добавление заявки на работу

        Args:
            session: Сессия базы данных
            data: Схема для заявки на работу

        Raises:
            JobNotFoundError: Работа не найдена
            ConflictException: Ошибка при добавлении заявки
        """

        job = await cls.repository.get_one_or_none(session, id=data.job_id)
        if not job:
            raise exceptions.JobNotFoundError()

        try:
            job.applications.append(data.employee_address)
            await session.commit()

        except Exception as e:
            raise exceptions.ConflictException(exc=e)

    # MARK: Get
    @classmethod
    async def get_applications(cls, session: AsyncSession, id: int) -> list[str]:
        """
        Получение списка заявок на работу

        Args:
            session: Сессия базы данных
            id: ID работы

        Returns:
            list[str]: Список заявок на работу

        Raises:
            JobNotFoundError: Работа не найдена
        """
        job = await cls.repository.get_one_or_none(session, id=id)
        if not job:
            raise exceptions.JobNotFoundError()

        return job.applications
