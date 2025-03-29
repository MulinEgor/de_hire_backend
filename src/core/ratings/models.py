"""Модуль для SQLAlchemy модели рейтингов"""

import enum
import uuid

from sqlalchemy import UUID, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class Role(enum.Enum):
    """Роли для рейтинга"""

    EMPLOYER = "Employer"
    EMPLOYEE = "Employee"


class Rating(Base):
    """SQLAlchemy модель рейтингов"""

    __tablename__ = "ratings"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))
    rated_person_address: Mapped[str] = mapped_column()
    score: Mapped[int] = mapped_column()
    role: Mapped[Role] = mapped_column(Enum(Role))
    comment: Mapped[str] = mapped_column()

    job: Mapped["Job"] = relationship(back_populates="ratings", foreign_keys=[job_id])
