"""Тесты для маршрутов резюме"""

import httpx

from src.api.resumes.router import router as resume_router
from src.core.jobs import Job
from src.core.resumes import Resume, ResumeGetSchema
from tests.integration.conftest import BaseTestRouter


class TestResumeRouter(BaseTestRouter):
    """Класс для тестов роутера резюме"""

    router = resume_router

    # MARK: Get
    async def test_get_resume(
        self,
        router_client: httpx.AsyncClient,
        resume_db: Resume,
        job_db: Job,
    ):
        """Тест на получение резюме"""
        response = await router_client.get(
            f"/resumes/{resume_db.person_address}/{resume_db.role.value}",
        )

        assert response.status_code == 200

        resume = ResumeGetSchema(**response.json())

        assert resume.name == resume_db.name
        assert resume.description == resume_db.description
        assert resume.years_of_experience >= 0
        assert resume.months_of_experience >= 0
        assert resume.ratings == []
        assert resume.skills != []
        assert resume.jobs != []
        assert resume.skills == job_db.skills
        assert resume.jobs[0].id == job_db.id
