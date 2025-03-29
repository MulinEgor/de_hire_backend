"""Модуль для сервиса резюме"""

from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from src.core import exceptions
from src.core.base import BaseService
from src.core.jobs import JobCreateSchema, JobPaginationSchema, JobService
from src.core.ratings import (
    RatingPaginationSchema,
    RatingService,
    RatingShortGetSchema,
    Role,
)
from src.core.resumes import schemas
from src.core.resumes.models import Resume
from src.core.resumes.repository import ResumeRepository


class ResumeService(
    BaseService[
        Resume,
        schemas.ResumeCreateSchema,
        schemas.ResumeGetSchema,
        schemas.ResumePaginationSchema,
        schemas.ResumeListReadSchema,
        schemas.ResumeCreateSchema,
    ]
):
    """Сервис для работы с резюме"""

    repository = ResumeRepository()

    @classmethod
    async def get_by_address_and_role(
        cls,
        session: AsyncSession,
        address: str,
        role: Role,
    ) -> schemas.ResumeGetSchema:
        """
        Получить резюме по адресу и роли

        Args:
            session (AsyncSession): Сессия для работы с базой данных.
            address (str): Адрес.
            role (Role): Роль.

        Returns:
            ResumeGetSchema: резюме.

        Raises:
            NotFoundException: Объект не найден.
        """

        resume = await cls.repository.get_one_or_none(
            session,
            Resume.person_address == address,
            Resume.role == role,
        )

        if not resume:
            raise exceptions.NotFoundException()

        try:
            jobs = await JobService.get(
                session,
                JobPaginationSchema(
                    employee_address=address,
                ),
            )
            jobs = [JobCreateSchema.model_validate(job) for job in jobs.data]

        except exceptions.NotFoundException:
            jobs = []

        try:
            ratings = await RatingService.get(
                session,
                RatingPaginationSchema(
                    person_address=address,
                    role=role,
                ),
            )
            ratings = [
                RatingShortGetSchema.model_validate(rating) for rating in ratings.data
            ]

        except exceptions.NotFoundException:
            ratings = []

        if jobs:
            skills = [skill for job in jobs for skill in job.skills]
            first_job = sorted(jobs, key=lambda x: x.created_at)[0]
            time_difference = datetime.now(timezone.utc) - first_job.created_at
            total_days = time_difference.days
            years_of_experience = total_days // 365
            months_of_experience = (total_days % 365) // 30
        else:
            skills = []
            years_of_experience, months_of_experience = 0, 0

        return schemas.ResumeGetSchema(
            name=resume.name,
            description=resume.description,
            years_of_experience=years_of_experience,
            months_of_experience=months_of_experience,
            skills=skills,
            ratings=ratings,
            jobs=jobs,
        )
