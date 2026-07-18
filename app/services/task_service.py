from fastapi import HTTPException
from datetime import date

from ..schemas import tasks
from ..fake_database import fake_vacancies_db, fake_tasks_db


async def does_vacancy_id_exists(vacancy_id : int):
    for vacancy in fake_vacancies_db:
        if vacancy["id"] == vacancy_id: return True
    return False

async def find_task_or_404(id : int):
    for task in fake_tasks_db:
        if task["id"] == id:
            return task
    raise HTTPException(status_code=404, detail="task not found")

async def find_vacancy_or_404(vacancy_id : int):
    for vacancy in fake_vacancies_db:
        if vacancy["id"] == vacancy_id:
            return vacancy
    raise HTTPException(status_code=404, detail="vacancy not found")

async def create_task(task : tasks.PreparationTaskCreate, vacancy_id : int):
    if not  await does_vacancy_id_exists(vacancy_id):
        raise HTTPException(status_code=404, detail="vacancy not found")
    id = max([b["id"] for b in fake_tasks_db], default=0) + 1
    task = task.model_dump()
    new_task = {"id" : id, "vacancy_id" : vacancy_id, **task, "is_done" : False}
    fake_tasks_db.append(new_task)
    return new_task

async def list_tasks(vacancy_id : int, id : int | None = None,
                     is_done : bool | None = None,
                     due_date : date | None = None):


    list_tasks = [b for b in fake_tasks_db if b["vacancy_id"] == vacancy_id]

    if id:
        list_tasks = [b for b in list_tasks if b["id"] == id]
    if is_done:
        list_tasks = [b for b in list_tasks if b["is_done"] == is_done]
    if due_date:
        list_tasks = [b for b in list_tasks if b["due_date"] == due_date]

    return list_tasks


async def delete_task (vacancy_id : int, task_id : int):
    vacancy = await find_vacancy_or_404(vacancy_id)
    task = await find_task_or_404(task_id)
    if task["vacancy_id"] != vacancy["id"]:
        raise HTTPException(status_code=400, detail="bad request")
    fake_tasks_db[:] = [b for b in fake_tasks_db if b != task]
    return
