"""Модуль для Pydantic схемы рейтинга"""

from pydantic import BaseModel

from src.base.schemas import DataListReadBaseSchema


class RatingSchema(BaseModel):
    """Схема рейтинга"""

    job_id: int
    rated_person_address: str
    score: int
    role: str
    comment: str


class RatingListReadSchema(DataListReadBaseSchema):
    """Схема для отображения списка рейтингов."""

    data: list[RatingSchema]
