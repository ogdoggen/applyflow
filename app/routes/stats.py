from fastapi import APIRouter

from ..services import stats_service

router = APIRouter(prefix = "/stats", tags = ["stats"])

@router.get("")
async def vacancies_stats():
    return await stats_service.vacancies_stats()
