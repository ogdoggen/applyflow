from fastapi import APIRouter
from datetime import date

from ..services import task_service
from ..schemas import tasks


router = APIRouter(prefix= "/vacancies", tags=["tasks"])

@router.post("/{vacancy_id}/tasks")
async def create_task(task : tasks.PreparationTaskCreate, vacancy_id : int):
    return await task_service.create_task(task, vacancy_id)

@router.get("/{vacancy_id}/tasks")
async def list_tasks(vacancy_id : int, id : int | None = None,
                     is_done : bool | None = None,
                     due_date : date | None = None):
    return await task_service.list_tasks(vacancy_id, id, is_done, due_date)

@router.delete("/{vacancy_id}/tasks/{task_id}")
async def delete_task(vacancy_id : int, task_id : int):
    return await task_service.delete_task(vacancy_id, task_id)