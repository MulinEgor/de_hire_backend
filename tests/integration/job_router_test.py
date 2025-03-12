"""Тесты для маршрутов работ"""

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from src.jobs import Job, JobGetSchema, JobListGetSchema
from src.jobs.router import router as job_router
from tests.integration.conftest import BaseTestRouter


class TestJobRouter(BaseTestRouter):
    """Класс для тестов роутера работ"""

    router = job_router

    # MARK: Get
    async def test_get_job(
        self,
        router_client: httpx.AsyncClient,
        job_db: Job,
    ):
        """Тест на получение работы по id"""
        response = await router_client.get(
            f"/jobs/{job_db.id}",
        )

        assert response.status_code == 200

        job = JobGetSchema(**response.json())

        assert job.id == job_db.id
        assert job.employer_address == job_db.employer_address
        assert job.employee_address == job_db.employee_address
        assert job.payment == job_db.payment
        assert job.deadline == job_db.deadline

    async def test_get_all_jobs(
        self,
        router_client: httpx.AsyncClient,
        job_db: Job,
    ):
        """Тест на получение всех работ"""
        response = await router_client.get(
            "/jobs",
        )

        assert response.status_code == 200

        jobs = JobListGetSchema(**response.json())

        assert len(jobs.data) == 1
        assert jobs.data[0].id == job_db.id
        assert jobs.data[0].employer_address == job_db.employer_address
        assert jobs.data[0].employee_address == job_db.employee_address
        assert jobs.data[0].payment == job_db.payment
        assert jobs.data[0].deadline == job_db.deadline
        assert jobs.data[0].status == job_db.status

    async def test_get_job_applications(
        self,
        router_client: httpx.AsyncClient,
        session: AsyncSession,
        job_db: Job,
    ):
        """Тест на получение заявок на работу"""

        job_db.applications = [
            "0x1234567890123456789012345678901234567890",
            "0x1234567890123456789012345678901234567891",
        ]

        await session.commit()

        response = await router_client.get(
            f"/jobs/{job_db.id}/applications",
        )

        assert response.status_code == 200

        assert response.json() == job_db.applications
