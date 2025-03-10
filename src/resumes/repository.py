"""Модуль для репозитория резюме"""

from src.base.repository import BaseRepository
from src.resumes.models import Resume
from src.resumes.schemas import ResumeSchema


class ResumeRepository(BaseRepository[Resume, ResumeSchema, ResumeSchema]):
    """Репозиторий резюме"""

    model = Resume
