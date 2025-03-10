"""Модуль для Pydantic схемы резюме"""

from pydantic import BaseModel

from src.base.schemas import DataListReadBaseSchema


class ResumeSchema(BaseModel):
    """Схема резюме"""

    person_address: str
    role: str
    name: str
    description: str


class ResumeListReadSchema(DataListReadBaseSchema):
    """Схема для отображения списка резюме."""

    data: list[ResumeSchema]
