"""Модуль для маршрутов рейтингов"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import src.base.schemas as base_schemas
import src.ratings.schemas as schemas
from src.dependencies import get_session
from src.ratings.models import Role
from src.ratings.service import RatingService

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
