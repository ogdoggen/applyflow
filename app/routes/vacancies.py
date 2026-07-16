from fastapi import APIRouter, HTTPException

from app.schemas.vacancies import Vacancy, VacancyCreate, VacancyRead, VacancyUpdate, VacancyStatus
from ..fake_database import fake_db

router = APIRouter(prefix = "/vacancies", tags = ["vacancies"])



@router.get("")
async def list_vacancies(status : VacancyStatus | None = None, company : str | None = None,
                         limit: int | None = None, offset : int | None = None):
    vacancies = [Vacancy(**b) for b in fake_db]

    if status:
        vacancies = [b for b in vacancies if b.status == status]

    if company:
        vacancies = [b for b in vacancies if b.company.lower() == company.lower()]

    if limit is not None:
        vacancies = vacancies[:limit]

    return vacancies

@router.get("/{vacancy_id}")
async def return_vacancy(vacancy_id:int):
    for vacancy in fake_db:
        if vacancy["id"] == vacancy_id:
            return vacancy
    raise HTTPException(
        status_code= 404,
        detail= "404. vacancy is not found"
    )

@router.post("", response_model= VacancyRead, status_code=201)
async def create_vacancy(vacancy : VacancyCreate):
    vacancy_id = max((existing_vacancy["id"] for existing_vacancy in fake_db), default=0) + 1
    new_vacancy = {"id" : vacancy_id, **vacancy.model_dump()}
    fake_db.append(new_vacancy)
    return new_vacancy


@router.patch("/{vacancy_id}", status_code=200)
async def update_vacancy(new_data: VacancyUpdate, vacancy_id: int):
    if vacancy_id == None:
        raise HTTPException(status_code=400, detail="enter vacancy id")

    updates = new_data.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(status_code=400, detail="no updates were provided")

    for vacancy in fake_db:
        if vacancy["id"] == vacancy_id:
            vacancy.update(updates)
            return vacancy

    raise HTTPException(status_code=404, detail="not found")

@router.delete("/{vacancy_id}", status_code=204)
async def delete_vacancy(vacancy_id : int):
    if vacancy_id == None:
        raise HTTPException(status_code=400, detail="enter vacancy id")
    else:
        for vacancy in fake_db:
            if vacancy["id"] == vacancy_id:
                fake_db.remove(vacancy)
                return
    raise HTTPException(status_code=404, detail="not found")
