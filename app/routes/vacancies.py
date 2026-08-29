from fastapi import APIRouter

from app.schemas.vacancies import Vacancy, VacancyCreate, VacancyRead, VacancyUpdate, VacancyStatus
from ..services import vacancy_service
from app.dependencies import db_session, CurrentUser

router = APIRouter(prefix = "/vacancies", tags = ["vacancies"])



@router.get("", response_model=list[VacancyRead])
async def list_vacancies(session : db_session, current_user : CurrentUser, status : VacancyStatus | None = None, company : str | None = None,
                         limit: int | None = None, offset : int | None = None):
    return await vacancy_service.list_vacancies(session = session, current_user=current_user, status = status, company = company, limit = limit, offset = offset)

@router.get("/{vacancy_id}", response_model=VacancyRead)
async def return_vacancy(session : db_session, current_user : CurrentUser, vacancy_id:int):
    return await vacancy_service.return_vacancy(session, current_user, vacancy_id)

@router.post("", response_model= VacancyRead, status_code=201)
async def create_vacancy(vacancy : VacancyCreate, session : db_session, current_user : CurrentUser):
    return await vacancy_service.create_vacancy(session = session, current_user=current_user, vacancy = vacancy)


@router.patch("/{vacancy_id}", status_code=200, response_model=VacancyRead)
async def update_vacancy(session : db_session, current_user : CurrentUser, new_data: VacancyUpdate, vacancy_id: int):
    return await vacancy_service.update_vacancy(session, current_user, new_data, vacancy_id)

@router.delete("/{vacancy_id}", status_code=204)
async def delete_vacancy(session : db_session, current_user : CurrentUser,vacancy_id : int):
    return await vacancy_service.delete_vacancy(session, current_user, vacancy_id)
