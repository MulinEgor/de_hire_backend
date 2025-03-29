"""Модуль для SQLAlchemy модели работы"""

import datetime
import enum

from sqlalchemy import ARRAY, DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class JobStatus(enum.Enum):
    """Статус работы"""

    OPEN = "Open"
    IN_PROGRESS = "InProgress"
    WAITING_REVIEW = "WaitingReview"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class Job(Base):
    """SQLAlchemy модель работы"""

    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    employer_address: Mapped[str] = mapped_column()
    employee_address: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[JobStatus] = mapped_column(Enum(JobStatus), default=JobStatus.OPEN)
    payment: Mapped[int] = mapped_column()
    deadline: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    description: Mapped[str] = mapped_column()
    skills: Mapped[list[str]] = mapped_column(ARRAY(String))
    applications: Mapped[list[str]] = mapped_column(ARRAY(String), default=[])
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now
    )

    ratings: Mapped[list["Rating"]] = relationship(back_populates="job")
