from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.vacancies import Vacancy, VacancyCreate, VacancyRead, VacancyUpdate, VacancyStatus
from app.models.vacancy import VacancyModel

async def find_vacancy_or_404(session : AsyncSession, vacancy_id : int):
    vacancy = await session.get(VacancyModel, vacancy_id)
    if vacancy is None:
        raise HTTPException(status_code=404, detail="vacancy not found")
    return vacancy


async def list_vacancies(session : AsyncSession, status : VacancyStatus | None = None, company : str | None = None,
                         limit: int | None = None, offset : int | None = None):

    async with (session.begin()):

        stmt = (select(VacancyModel))
        if status is not None:
            stmt = stmt.where(VacancyModel.status == status)

        if company is not None:
            stmt = stmt.where(VacancyModel.company.ilike(company))

        stmt = (stmt.order_by(VacancyModel.id)
                .limit(limit)
                .offset(offset))
        result = await session.scalars(stmt)
        return result.all()

async def return_vacancy(session : AsyncSession, vacancy_id : int):
    return await find_vacancy_or_404(session, vacancy_id)

async def create_vacancy(session : AsyncSession, vacancy : VacancyCreate):

    new_vacancy = VacancyModel(company=vacancy.company, title = vacancy.title,
                                url = str(vacancy.url) ,
                               status = vacancy.status,
                                description = vacancy.description)
    session.add(new_vacancy)
    try:
        await session.commit()
        await session.refresh(new_vacancy)
    except SQLAlchemyError:
        await session.rollback()
        raise
    return new_vacancy



async def update_vacancy(session : AsyncSession, new_data: VacancyUpdate, vacancy_id: int):

    vacancy = await find_vacancy_or_404(session, vacancy_id)
    updates = new_data.model_dump(exclude_unset=True, mode="json")
    if not updates:
        raise HTTPException(status_code=400, detail="no updates were provided")
    for field, value in updates.items():
        setattr(vacancy, field, value)
    try:
        await session.commit()
        await session.refresh(vacancy)
    except SQLAlchemyError:
        await session.rollback()
        raise
    return vacancy


async def delete_vacancy(session : AsyncSession, vacancy_id : int):

    vacancy = await find_vacancy_or_404(session, vacancy_id)
    try:
        await session.delete(vacancy)
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise
    return
