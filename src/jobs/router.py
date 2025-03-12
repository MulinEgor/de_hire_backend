"""Модуль для роутера работ"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_session
from src.jobs import JobPaginationSchema, JobService

router = APIRouter(prefix="/jobs", tags=["Работы"])


@router.get("/{id}")
async def get_job(id: int, session: AsyncSession = Depends(get_session)):
    """Получение работы по id"""

    return await JobService.get_by_id(session, id)


@router.get("")
async def get_jobs(
    query_params: JobPaginationSchema = Depends(),
    session: AsyncSession = Depends(get_session),
):
    """Получение списка работ"""

    return await JobService.get(session, query_params)


@router.get("/{id}/applications")
async def get_job_applications(id: int, session: AsyncSession = Depends(get_session)):
    """Получение списка заявок на работу"""

    return await JobService.get_applications(session, id)
