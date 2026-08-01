from fastapi import APIRouter

from app.schemas.vacancies import Vacancy, VacancyCreate, VacancyRead, VacancyUpdate, VacancyStatus
from ..services import vacancy_service
from app.dependencies import db_session

router = APIRouter(prefix = "/vacancies", tags = ["vacancies"])



@router.get("", response_model=list[VacancyRead])
async def list_vacancies(session : db_session, status : VacancyStatus | None = None, company : str | None = None,
                         limit: int | None = None, offset : int | None = None):
    return await vacancy_service.list_vacancies(session = session, status = status, company = company, limit = limit, offset = offset)

@router.get("/{vacancy_id}")
async def return_vacancy(vacancy_id:int):
    return await vacancy_service.return_vacancy(vacancy_id)

@router.post("", response_model= VacancyRead, status_code=201)
async def create_vacancy(vacancy : VacancyCreate, session : db_session):
    return await vacancy_service.create_vacancy(session = session, vacancy = vacancy)


@router.patch("/{vacancy_id}", status_code=200)
async def update_vacancy(new_data: VacancyUpdate, vacancy_id: int):
    return await vacancy_service.update_vacancy(new_data, vacancy_id)

@router.delete("/{vacancy_id}", status_code=204)
async def delete_vacancy(vacancy_id : int):
    return await vacancy_service.delete_vacancy(vacancy_id)
