"""Модуль для репозитория резюме"""

from typing import Tuple

from sqlalchemy import Select, and_, select

from src.base.repository import BaseRepository
from src.resumes import schemas
from src.resumes.models import Resume


class ResumeRepository(
    BaseRepository[Resume, schemas.ResumeCreateSchema, schemas.ResumeCreateSchema]
):
    """Репозиторий резюме"""

    model = Resume

    @classmethod
    async def get_stmt_by_query(
        cls,
        query_params: schemas.ResumePaginationSchema,
    ) -> Select[Tuple[Resume]]:
        """
        Создать подготовленное выражение для запроса в БД,
        применив основные query параметры без учета пагинации,
        для получения списка пользователей.

        Args:
            query_params (ResumePaginationSchema): параметры для запроса.

        Returns:
            stmt: Подготовленное выражение для запроса в БД.
        """

        stmt = select(Resume)

        # Фильтрация по username с использованием ilike.
        stmt = stmt.where(
            and_(
                Resume.person_address == query_params.person_address,
                Resume.role == query_params.role,
            )
        )

        return stmt
