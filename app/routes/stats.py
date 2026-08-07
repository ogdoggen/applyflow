from fastapi import APIRouter

from ..services import stats_service
from app.dependencies import db_session

router = APIRouter(prefix = "/stats", tags = ["stats"])

@router.get("")
async def vacancies_stats(session : db_session):
    return await stats_service.vacancies_stats(session)
