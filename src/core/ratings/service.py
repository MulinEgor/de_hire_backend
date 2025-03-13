"""Модуль для сервиса рейтингов"""

import src.core.ratings.schemas as schemas
from src.core.base import BaseService
from src.core.ratings.models import Rating
from src.core.ratings.repository import RatingRepository


class RatingService(
    BaseService[
        Rating,
        schemas.RatingSchema,
        schemas.RatingSchema,
        schemas.RatingPaginationSchema,
        schemas.RatingListReadSchema,
        schemas.RatingSchema,
    ]
):
    """Сервис для работы с рейтингами"""

    repository = RatingRepository()
