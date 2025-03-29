"""Модуль для репозитория работы"""

from typing import Tuple

from sqlalchemy import Select, select

from src.core.base import BaseRepository, PaginationBaseSchema
from src.core.ratings import schemas
from src.core.ratings.models import Rating


class RatingRepository(
    BaseRepository[Rating, schemas.RatingSchema, schemas.RatingSchema]
):
    """Репозиторий рейтингов"""

    model = Rating

    @classmethod
    async def get_stmt_by_query(
        cls,
        query_params: schemas.RatingPaginationSchema | PaginationBaseSchema,
    ) -> Select[Tuple[Rating]]:
        """
        Создать подготовленное выражение для запроса в БД,
        применив основные query параметры без учета пагинации,
        для получения списка пользователей.

        Args:
            query_params (ResumePaginationSchema | PaginationBaseSchema):
                параметры для запроса.

        Returns:
            stmt: Подготовленное выражение для запроса в БД.
        """

        stmt = select(Rating)

        # Фильтрация
        if isinstance(query_params, schemas.RatingPaginationSchema):
            stmt = stmt.where(
                Rating.rated_person_address == query_params.person_address,
            )

        if isinstance(query_params, schemas.RatingPaginationSchema):
            stmt = stmt.where(
                Rating.role == query_params.role,
            )

        return stmt
