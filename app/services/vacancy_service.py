from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.vacancies import Vacancy, VacancyCreate, VacancyRead, VacancyUpdate, VacancyStatus
from ..fake_database import fake_vacancies_db, fake_tasks_db
from app.models.vacancy import VacancyModel

async def find_vacancy_or_404(session : AsyncSession, vacancy_id : int):
    vacancy = await session.get(VacancyModel, vacancy_id)
    if vacancy is None:
        raise HTTPException(status_code=404, detail="vacancy not found")
    return vacancy

async def does_id_exists(vacancy_id : int):
    for vacancy in fake_vacancies_db:
        if vacancy["id"] == vacancy_id:
            return True
    return False

async def list_vacancies(session : AsyncSession ,status : VacancyStatus | None = None, company : str | None = None,
                         limit: int | None = None, offset : int | None = None):
    # vacancies = [VacancyRead(**b) for b in fake_vacancies_db]
    #
    # if status is not None:
    #     vacancies = [b for b in vacancies if b.status == status]
    #
    # if company is not None:
    #     vacancies = [b for b in vacancies if b.company.lower() == company.lower()]
    #
    # if limit is not None:
    #     vacancies = vacancies[:limit]
    #
    # return vacancies

    async with session.begin():
        smth = select(VacancyModel).order_by(VacancyModel.id)
        result = await session.scalars(smth)
        return result.all()

async def return_vacancy(session : AsyncSession, vacancy_id : int):
    return await find_vacancy_or_404(session, vacancy_id)

async def create_vacancy(session : AsyncSession, vacancy : VacancyCreate):
    # vacancy_id = max((existing_vacancy["id"] for existing_vacancy in fake_vacancies_db), default=0) + 1
    # new_vacancy = {"id" : vacancy_id, **vacancy.model_dump()}
    # fake_vacancies_db.append(new_vacancy)
    # return new_vacancy

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

    # vacancy = await find_vacancy_or_404(vacancy_id)
    # updates = new_data.model_dump(exclude_unset=True)
    # if not updates:
    #     raise HTTPException(status_code=400, detail="no updates were provided")
    # for item in fake_vacancies_db:
    #     if item == vacancy:
    #         item.update(updates)
    #         return item
    # raise HTTPException(status_code=400, detail="bad request")

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
    # vacancy = await find_vacancy_or_404(vacancy_id)
    # for item in fake_vacancies_db:
    #     if item == vacancy:
    #         fake_vacancies_db.remove(item)
    #         await delete_all_tasks_for_vacancy(vacancy_id)
    #         return
    # raise HTTPException(status_code=404, detail="not found")
    vacancy = await find_vacancy_or_404(session, vacancy_id)
    try:
        await session.delete(vacancy)
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise
    return

async def delete_all_tasks_for_vacancy(vacancy_id : int):
    fake_tasks_db[:] = [task for task in fake_tasks_db if task["vacancy_id"] != vacancy_id]
