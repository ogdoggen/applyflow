from fastapi import APIRouter
from datetime import date

from ..services import task_service
from ..schemas import tasks
from app.dependencies import db_session


router = APIRouter(prefix= "/vacancies", tags=["tasks"])

@router.post("/{vacancy_id}/tasks", response_model=tasks.PreparationTaskRead, status_code=201)
async def create_task(session : db_session,task : tasks.PreparationTaskCreate, vacancy_id : int):
    return await task_service.create_task(session, task, vacancy_id)

@router.get("/{vacancy_id}/tasks", response_model=list[tasks.PreparationTaskRead])
async def list_tasks(session : db_session, vacancy_id : int, task_id : int | None = None,
                     is_done : bool | None = None,
                     due_date : date | None = None):
    return await task_service.list_tasks(session, vacancy_id, task_id, is_done, due_date)

@router.get("/{vacancy_id}/tasks/{task_id}", response_model=tasks.PreparationTaskRead)
async def return_task(session : db_session, vacancy_id : int, task_id : int):
    return await task_service.return_task(session, vacancy_id, task_id)

@router.delete("/{vacancy_id}/tasks/{task_id}", status_code=204)
async def delete_task(session : db_session, vacancy_id : int, task_id : int):
    return await task_service.delete_task(session, vacancy_id, task_id)

@router.patch("/{vacancy_id}/tasks/{task_id}", response_model=tasks.PreparationTaskRead)
async def update_task(session : db_session, vacancy_id : int, task_id : int, updates : tasks.PreparationTaskUpdate):
    return await task_service.update_task(session, vacancy_id, task_id, updates)