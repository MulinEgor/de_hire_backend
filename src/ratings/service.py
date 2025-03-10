"""Модуль для сервиса рейтингов"""

import src.base.schemas as base_schemas
import src.ratings.schemas as schemas
from src.base.service import BaseService
from src.ratings.models import Rating
from src.ratings.repository import RatingRepository


class JobService(
    BaseService[
        Rating,
        schemas.RatingSchema,
        schemas.RatingSchema,
        base_schemas.PaginationBaseSchema,
        schemas.RatingListReadSchema,
        schemas.RatingSchema,
    ]
):
    """Сервис для работы с рейтингами"""

    repository = RatingRepository()
