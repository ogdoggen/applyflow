from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.vacancy import VacancyModel
from app.models.user import UserModel

async def vacancies_stats(session : AsyncSession, cur_user : UserModel):

    stmt1 = select(func.count()).select_from(VacancyModel).where(VacancyModel.owner_id == cur_user.id)
    stmt2 = select(VacancyModel.status, func.count()).where(VacancyModel.owner_id == cur_user.id).group_by(VacancyModel.status)
    total = await session.scalar(stmt1)
    by_status = (await session.execute(stmt2)).all()

    return {"total vacancies number" : total, "by status" : [{row.status : row.count} for row in by_status]}
