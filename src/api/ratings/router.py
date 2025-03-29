"""Модуль для маршрутов рейтингов"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import src.core.base.schemas as base_schemas
import src.core.ratings.schemas as schemas
from src.api.dependencies import get_session
from src.core.ratings.models import Role
from src.core.ratings.service import RatingService

router = APIRouter(prefix="/ratings", tags=["Рейтинги"])


@router.get("/{person_address}/{role}")
async def get_ratings(
    person_address: str,
    role: Role,
    pagination: base_schemas.PaginationBaseSchema = Depends(),
    session: AsyncSession = Depends(get_session),
) -> schemas.RatingListReadSchema:
    """Получение рейтингов по адресу и роли"""

    return await RatingService.get(
        session,
        schemas.RatingPaginationSchema(
            person_address=person_address,
            role=role,
            **pagination.model_dump(),
        ),
    )


@router.get("")
async def get_all_ratings(
    pagination: base_schemas.PaginationBaseSchema = Depends(),
    session: AsyncSession = Depends(get_session),
) -> schemas.RatingListReadSchema:
    """Получение всех рейтингов"""

    return await RatingService.get(session, pagination)
