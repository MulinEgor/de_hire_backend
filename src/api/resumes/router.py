"""Модуль для маршрутов резюме"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import src.core.resumes.schemas as schemas
from src.api.dependencies import get_session
from src.core.ratings.models import Role
from src.core.resumes.service import ResumeService

router = APIRouter(prefix="/resumes", tags=["Резюме"])


@router.get("/{person_address}/{role}")
async def get_resume(
    person_address: str,
    role: Role,
    session: AsyncSession = Depends(get_session),
) -> schemas.ResumeGetSchema:
    """Получение резюме по адресу и роли"""

    return await ResumeService.get_by_address_and_role(
        session,
        person_address,
        role,
    )
