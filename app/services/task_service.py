from fastapi import HTTPException
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from app.models.task import PreparationTaskModel
from ..models import VacancyModel


from ..schemas import tasks
from ..fake_database import fake_vacancies_db, fake_tasks_db


async def does_vacancy_id_exists(vacancy_id : int):
    for vacancy in fake_vacancies_db:
        if vacancy["id"] == vacancy_id: return True
    return False

async def find_task_or_404(session : AsyncSession, task_id : int):
    # for task in fake_tasks_db:
    #     if task["id"] == id:
    #         return task
    # raise HTTPException(status_code=404, detail="task not found")
    task = await session.get(PreparationTaskModel, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    return task

async def find_vacancy_or_404(session : AsyncSession, vacancy_id : int):
    vacancy = await session.get(VacancyModel, vacancy_id)
    if vacancy is None:
        raise HTTPException(status_code=404, detail="vacancy not found")
    return vacancy

async def create_task(session : AsyncSession, task : tasks.PreparationTaskCreate, vacancy_id : int):
    # if not  await does_vacancy_id_exists(vacancy_id):
    #     raise HTTPException(status_code=404, detail="vacancy not found")
    # id = max([b["id"] for b in fake_tasks_db], default=0) + 1
    # task = task.model_dump()
    # new_task = {"id" : id, "vacancy_id" : vacancy_id, **task, "is_done" : False}
    # fake_tasks_db.append(new_task)
    # return new_task

    new_task = PreparationTaskModel(vacancy_id = vacancy_id,
                                    title = task.title,
                                    is_done = False,
                                    due_date = task.due_date)
    if task.notes is not None:
        new_task.notes = task.notes

    session.add(new_task)
    try:
        await session.commit()
        await session.refresh(new_task)
    except SQLAlchemyError:
        await session.rollback()
        raise
    return new_task


async def list_tasks(session : AsyncSession, vacancy_id : int, task_id : int | None = None,
                     is_done : bool | None = None,
                     due_date : date | None = None):

    await find_vacancy_or_404(session, vacancy_id)

    stmt = (select(PreparationTaskModel))
    stmt = stmt.where(PreparationTaskModel.vacancy_id == vacancy_id)
    if task_id is not None:
        stmt = stmt.where(PreparationTaskModel.id == task_id)
    if is_done is not None:
        stmt = stmt.where(PreparationTaskModel.is_done == is_done)
    if due_date is not None:
        stmt = stmt.where(PreparationTaskModel.due_date == due_date)
    stmt = stmt.order_by(PreparationTaskModel.id)
    result = await session.scalars(stmt)
    return result.all()

async def return_task(session : AsyncSession, vacancy_id : int, task_id : int):
    await find_vacancy_or_404(session, vacancy_id)
    task = await find_task_or_404(session, task_id)
    return task

async def delete_task (session : AsyncSession, vacancy_id : int, task_id : int):
    # vacancy = await find_vacancy_or_404(vacancy_id)
    # task = await find_task_or_404(task_id)
    # if task["vacancy_id"] != vacancy["id"]:
    #     raise HTTPException(status_code=400, detail="bad request")
    # fake_tasks_db[:] = [b for b in fake_tasks_db if b != task]
    # return
    await find_vacancy_or_404(session, vacancy_id)
    task = await find_task_or_404(session, task_id)
    await session.delete(task)
    try:
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise
    return

async def update_task(session : AsyncSession,
                      vacancy_id : int,
                      task_id : int,
                      new_data : tasks.PreparationTaskUpdate):
    await find_vacancy_or_404(session, vacancy_id)
    task = await find_task_or_404(session, task_id)
    updates = new_data.model_dump(mode="json", exclude_unset=True)
    if updates is None:
        raise HTTPException(status_code=400, detail="no updates were provided")
    for attr, value in updates.items():
        setattr(task, attr, value)
    try:
        await session.commit()
        await session.refresh(task)
    except SQLAlchemyError:
        await session.rollback()
        raise
    return task