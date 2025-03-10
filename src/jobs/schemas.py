"""Модуль для Pydantic схемы работы"""

from datetime import datetime

from pydantic import BaseModel

from src.base.schemas import DataListReadBaseSchema


class JobSchema(BaseModel):
    """Схема работы"""

    employer_address: str
    employee_address: str
    status: str
    payment: int
    deadline: datetime
    description: str
    skills: list[str]


class JobListReadSchema(DataListReadBaseSchema):
    """Схема для отображения списка работ."""

    data: list[JobSchema]
