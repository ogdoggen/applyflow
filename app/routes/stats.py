from fastapi import APIRouter

from ..services import stats_service
from app.dependencies import db_session, CurrentUser

router = APIRouter(prefix = "/stats", tags = ["stats"])

@router.get("")
async def vacancies_stats(session : db_session, cur_user : CurrentUser):
    return await stats_service.vacancies_stats(session, cur_user)
