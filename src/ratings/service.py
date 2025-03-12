"""Модуль для сервиса рейтингов"""

import src.ratings.schemas as schemas
from src.base.service import BaseService
from src.ratings.models import Rating
from src.ratings.repository import RatingRepository


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
