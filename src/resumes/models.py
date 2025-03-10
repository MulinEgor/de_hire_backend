"""Модуль для SQLAlchemy модели рейтингов"""

import uuid

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Resume(Base):
    """SQLAlchemy модель рейтингов"""

    __tablename__ = "resumes"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    person_address: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
