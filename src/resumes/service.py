"""Модуль для сервиса резюме"""

import src.base.schemas as base_schemas
import src.resumes.schemas as schemas
from src.base.service import BaseService
from src.resumes.models import Resume
from src.resumes.repository import ResumeRepository


class JobService(
    BaseService[
        Resume,
        schemas.ResumeSchema,
        schemas.ResumeSchema,
        base_schemas.PaginationBaseSchema,
        schemas.ResumeListReadSchema,
        schemas.ResumeSchema,
    ]
):
    """Сервис для работы с резюме"""

    repository = ResumeRepository()
