"""Тесты для маршрутов рейтингов"""

import httpx

from src.ratings import Rating, RatingListReadSchema
from src.ratings.router import router as rating_router
from tests.integration.conftest import BaseTestRouter


class TestRatingRouter(BaseTestRouter):
    """Класс для тестов роутера рейтингов"""

    router = rating_router

    # MARK: Get
    async def test_get_rating_for_person(
        self,
        router_client: httpx.AsyncClient,
        rating_db: Rating,
    ):
        """Тест на получение рейтинга для конкретного человека"""
        response = await router_client.get(
            f"/ratings/{rating_db.rated_person_address}/{rating_db.role.value}",
        )

        assert response.status_code == 200

        rating = RatingListReadSchema(**response.json())

        assert len(rating.data) == 1
        assert rating.data[0].job_id == rating_db.job_id
        assert rating.data[0].rated_person_address == rating_db.rated_person_address
        assert rating.data[0].score == rating_db.score
        assert rating.data[0].comment == rating_db.comment
        assert rating.data[0].role == rating_db.role

    async def test_get_all_ratings(
        self,
        router_client: httpx.AsyncClient,
        rating_db: Rating,
    ):
        """Тест на получение всех рейтингов"""
        response = await router_client.get(
            "/ratings",
        )

        assert response.status_code == 200

        ratings = RatingListReadSchema(**response.json())

        assert len(ratings.data) == 1
        assert ratings.data[0].job_id == rating_db.job_id
        assert ratings.data[0].rated_person_address == rating_db.rated_person_address
        assert ratings.data[0].score == rating_db.score
        assert ratings.data[0].comment == rating_db.comment
        assert ratings.data[0].role == rating_db.role
