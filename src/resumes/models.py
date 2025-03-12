"""Модуль для SQLAlchemy модели резюме"""

import uuid

from sqlalchemy import UUID, Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.ratings.models import Role


class Resume(Base):
    """SQLAlchemy модель резюме"""

    __tablename__ = "resumes"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    person_address: Mapped[str] = mapped_column()
    role: Mapped[Role] = mapped_column(Enum(Role))
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
