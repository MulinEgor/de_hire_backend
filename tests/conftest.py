"""Основной модуль `conftest` для всех тестов."""

import asyncio
import datetime
import random
import sys
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from faker import Faker
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.jobs import Job, JobGetSchema, JobRepository, JobStatus
from src.core.ratings import Rating, RatingRepository, RatingSchema, Role
from src.core.resumes import Resume, ResumeCreateSchema, ResumeRepository
from src.core.settings import settings

faker = Faker()


# MARK: DBSession
@pytest_asyncio.fixture(scope="module")
async def engine(request, worker_id) -> AsyncGenerator[AsyncEngine, None]:
    """
    Создает экземпляр `AsyncEngine' с URL-адресом базы данных,
    соответствующим процессу pytest.

    Область действия `module` задается, поскольку каждый модуль c тестами
    выполняется в отдельном процессе pytest, чтобы гарантировать, что
    он подключается к соответствующей базе данных.
    """

    engine = create_async_engine(
        url=(
            f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
            f"{settings.POSTGRES_HOST}-{worker_id}:{settings.POSTGRES_PORT}/{worker_id}"
        ),
        poolclass=NullPool,
    )

    yield engine


@pytest.fixture(scope="function")
async def session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """
    Создать соединение с Postgres, начать транзакцию,
    а затем привязать это соединение к сессии с вложенной транзакцией.

    Вложенная транзакция обеспечивает изоляцию внутри тестов, позволяя
    фиксировать изменения во внутренней транзакции так, чтобы они были
    видны только для тестов, где она используется, но не фиксировать их
    в БД полностью, поскольку коммит внешней транзакции
    никогда не будет выполнен.

    Параметр `scope="function"` обеспечивает запуск этой фикстуры перед запуском каждого
    теста. Так что после запуска каждого теста, данные в БД откатываются.
    Каждый тест работает изолированно от других.

    Используется движок, соответствующий процессу `pytest`.
    """

    AsyncSession = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    async with engine.connect() as conn:
        tsx = await conn.begin()
        async with AsyncSession(bind=conn) as session:
            nested_tsx = await conn.begin_nested()

            yield session

            if nested_tsx.is_active:
                await nested_tsx.rollback()
            await tsx.rollback()


@pytest.fixture()
async def task_session(
    session: AsyncSession,
    mocker,
) -> AsyncSession:
    """Мокирование сессии для выполнения задач Celery."""

    async def mock_get_session():
        yield session

    mocker.patch("tasks.db_session.get_session", return_value=mock_get_session())
    return session


# MARK: Loop
@pytest.fixture(scope="session")
def event_loop(request):
    """
    Фикстура для создания и закрытия event loop.
    """

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# MARK: Output
@pytest.fixture(autouse=True, scope="session")
def output_to_stdout():
    """
    Перенаправить `stdout` в `stderr`,
    для вывода логов при отладки в `pytest-xdist`.
    """

    sys.stdout = sys.stderr


# MARK: Jobs
@pytest.fixture()
async def job_db(session: AsyncSession) -> Job:
    """Создание работы в базе данных"""

    job = await JobRepository.create(
        session,
        JobGetSchema(
            id=random.randint(1, 1000),
            employer_address=faker.word(),
            payment=random.randint(1, 1000),
            deadline=faker.date_time(),
            description=faker.text(),
            skills=[faker.word() for _ in range(random.randint(1, 10))],
            applications=[],
            employee_address=faker.word(),
            status=JobStatus.COMPLETED,
            created_at=faker.date_time(end_datetime=datetime.datetime.now()),
        ),
    )

    await session.commit()

    return job


# MARK: Resumes
@pytest.fixture()
async def resume_db(session: AsyncSession, job_db: Job) -> Resume:
    """Создание резюме в базе данных"""

    resume = await ResumeRepository.create(
        session,
        ResumeCreateSchema(
            person_address=job_db.employee_address,
            role=Role.EMPLOYEE,
            name=faker.name(),
            description=faker.text(),
        ),
    )

    await session.commit()

    return resume


# MARK: Ratings
@pytest.fixture()
async def rating_db(session: AsyncSession, job_db: Job) -> Rating:
    """Создание рейтинга в базе данных"""

    rating = await RatingRepository.create(
        session,
        RatingSchema(
            job_id=job_db.id,
            rated_person_address=job_db.employee_address,
            score=random.randint(1, 5),
            comment=faker.text(),
            role=Role.EMPLOYEE,
        ),
    )

    await session.commit()

    return rating
