"""Модуль для SQLAlchemy модели работы"""

import datetime
import uuid

from sqlalchemy import ARRAY, UUID, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Job(Base):
    """SQLAlchemy модель работы"""

    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    employer_address: Mapped[str] = mapped_column()
    employee_address: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column()
    payment: Mapped[int] = mapped_column()
    deadline: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    description: Mapped[str] = mapped_column()
    skills: Mapped[list[str]] = mapped_column(ARRAY(String))
