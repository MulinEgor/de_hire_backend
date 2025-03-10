"""Модуль для сервиса работы"""

import src.base.schemas as base_schemas
import src.jobs.schemas as schemas
from src.base.service import BaseService
from src.jobs.models import Job
from src.jobs.repository import JobRepository


class JobService(
    BaseService[
        Job,
        schemas.JobSchema,
        schemas.JobSchema,
        base_schemas.PaginationBaseSchema,
        schemas.JobListReadSchema,
        schemas.JobSchema,
    ]
):
    """Сервис работы"""

    repository = JobRepository()
