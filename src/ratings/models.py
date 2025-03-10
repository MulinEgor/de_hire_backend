"""Модуль для SQLAlchemy модели рейтингов"""

import uuid

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Rating(Base):
    """SQLAlchemy модель рейтингов"""

    __tablename__ = "ratings"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    job_id: Mapped[int] = mapped_column()
    rated_person_address: Mapped[str] = mapped_column()
    score: Mapped[int] = mapped_column()
    role: Mapped[str] = mapped_column()
    comment: Mapped[str] = mapped_column()
