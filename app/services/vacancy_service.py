from fastapi import HTTPException

from app.schemas.vacancies import Vacancy, VacancyCreate, VacancyRead, VacancyUpdate, VacancyStatus
from ..fake_database import fake_vacancies_db, fake_tasks_db

async def find_vacancy_or_404(vacancy_id : int):
    for vacancy in fake_vacancies_db:
        if vacancy["id"] == vacancy_id:
            return vacancy
    raise HTTPException(status_code=404, detail="vacancy not found")

async def does_id_exists(vacancy_id : int):
    for vacancy in fake_vacancies_db:
        if vacancy["id"] == vacancy_id:
            return True
    return False

async def list_vacancies(status : VacancyStatus | None = None, company : str | None = None,
                         limit: int | None = None, offset : int | None = None):
    vacancies = [VacancyRead(**b) for b in fake_vacancies_db]

    if status is not None:
        vacancies = [b for b in vacancies if b.status == status]

    if company is not None:
        vacancies = [b for b in vacancies if b.company.lower() == company.lower()]

    if limit is not None:
        vacancies = vacancies[:limit]

    return vacancies

async def return_vacancy(vacancy_id : int):
    return await find_vacancy_or_404(vacancy_id)

async def create_vacancy(vacancy : VacancyCreate):
    vacancy_id = max((existing_vacancy["id"] for existing_vacancy in fake_vacancies_db), default=0) + 1
    new_vacancy = {"id" : vacancy_id, **vacancy.model_dump()}
    fake_vacancies_db.append(new_vacancy)
    return new_vacancy

async def update_vacancy(new_data: VacancyUpdate, vacancy_id: int):

    vacancy = await find_vacancy_or_404(vacancy_id)
    updates = new_data.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=400, detail="no updates were provided")
    for item in fake_vacancies_db:
        if item == vacancy:
            item.update(updates)
            return item
    raise HTTPException(status_code=400, detail="bad request")


async def delete_vacancy(vacancy_id : int):
    vacancy = await find_vacancy_or_404(vacancy_id)
    for item in fake_vacancies_db:
        if item == vacancy:
            fake_vacancies_db.remove(item)
            await delete_all_tasks_for_vacancy(vacancy_id)
            return
    raise HTTPException(status_code=404, detail="not found")

async def delete_all_tasks_for_vacancy(vacancy_id : int):
    fake_tasks_db[:] = [task for task in fake_tasks_db if task["vacancy_id"] != vacancy_id]
