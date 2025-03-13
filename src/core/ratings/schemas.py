"""Модуль для Pydantic схемы рейтинга"""

from pydantic import BaseModel, Field

from src.core.base import DataListReadBaseSchema, PaginationBaseSchema
from src.core.ratings.models import Role


class RatingSchema(BaseModel):
    """Схема рейтинга"""

    job_id: int = Field(alias="jobId")
    rated_person_address: str = Field(alias="ratedPersonAddress")
    score: int
    role: Role
    comment: str

    model_config = {"from_attributes": True, "populate_by_name": True}


class RatingShortGetSchema(BaseModel):
    """Схема для получения краткого рейтинга"""

    job_id: int = Field(alias="jobId")
    score: int
    role: Role
    comment: str

    model_config = {"from_attributes": True, "populate_by_name": True}


class RatingPaginationSchema(PaginationBaseSchema):
    """Схема для пагинации рейтингов"""

    person_address: str
    role: Role


class RatingListReadSchema(DataListReadBaseSchema):
    """Схема для отображения списка рейтингов."""

    data: list[RatingSchema]
