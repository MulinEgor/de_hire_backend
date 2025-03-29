"""Модуль для Pydantic схемы работы"""

from datetime import datetime

from pydantic import BaseModel, Field

from src.core.base import DataListReadBaseSchema, PaginationBaseSchema
from src.core.jobs.models import JobStatus


class JobCreateSchema(BaseModel):
    """Схема для создания работы"""

    id: int = Field(alias="jobId")
    employer_address: str = Field(alias="employerAddress")
    payment: int
    deadline: datetime
    description: str
    skills: list[str]

    model_config = {"from_attributes": True, "populate_by_name": True}


class JobGetSchema(JobCreateSchema):
    """Схема для получения работы"""

    employee_address: str = Field(alias="employeeAddress")
    status: JobStatus
    applications: list[str]
    created_at: datetime

    model_config = {"from_attributes": True, "populate_by_name": True}


class JobUpdateSchema(BaseModel):
    """Схема для обновления работы"""

    job_id: str = Field(alias="jobId")
    employee_address: str | None = Field(None, alias="employeeAddress")
    status: JobStatus | None = None

    model_config = {"from_attributes": True, "populate_by_name": True}


class JobApplicationSchema(BaseModel):
    """Схема для заявки на работу"""

    job_id: str = Field(alias="jobId")
    employee_address: str = Field(alias="employeeAddress")

    model_config = {"from_attributes": True, "populate_by_name": True}


class JobPaginationSchema(PaginationBaseSchema):
    """Схема для пагинации работ"""

    employer_address: str | None = None
    employee_address: str | None = None


class JobListGetSchema(DataListReadBaseSchema):
    """Схема для отображения списка работ."""

    data: list[JobGetSchema]
