"""Модуль для репозитория работы"""

from src.base.repository import BaseRepository
from src.jobs.models import Job
from src.jobs.schemas import JobSchema


class JobRepository(BaseRepository[Job, JobSchema, JobSchema]):
    """Репозиторий работы"""

    model = Job
