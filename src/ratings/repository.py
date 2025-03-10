"""Модуль для репозитория работы"""

from src.base.repository import BaseRepository
from src.ratings.models import Rating
from src.ratings.schemas import RatingSchema


class RatingRepository(BaseRepository[Rating, RatingSchema, RatingSchema]):
    """Репозиторий рейтингов"""

    model = Rating
