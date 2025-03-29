"""Модуль для Pydantic схемы резюме"""

from pydantic import BaseModel, Field

from src.core.base import DataListReadBaseSchema, PaginationBaseSchema
from src.core.jobs.schemas import JobCreateSchema
from src.core.ratings.models import Role
from src.core.ratings.schemas import RatingShortGetSchema


class ResumeCreateSchema(BaseModel):
    """Схема резюме"""

    person_address: str = Field(alias="personAddress")
    role: Role
    name: str
    description: str

    model_config = {"from_attributes": True, "populate_by_name": True}


class ResumeGetSchema(BaseModel):
    """Схема для получения резюме"""

    name: str
    description: str
    years_of_experience: int
    months_of_experience: int
    skills: list[str]
    ratings: list[RatingShortGetSchema]
    jobs: list[JobCreateSchema]


class ResumePaginationSchema(PaginationBaseSchema):
    """Схема для пагинации резюме"""

    person_address: str
    role: Role


class ResumeListReadSchema(DataListReadBaseSchema):
    """Схема для отображения списка резюме."""

    data: list[ResumeGetSchema]
