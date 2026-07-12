from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pygments.lexer import default

from app.schemas.vacancies import Vacancy, VacancyCreate, VacancyRead, VacancyUpdate, VacancyStatus

vacancies = ["python backend", "go backend", "devops", "cyber security"]
fake_db = [
    {
        "id" : 1, "company": "Yandex", "title" : "python backend",
        "url" : "https://yandex.ru/backend/internship", "status" : "applied",
        "description" : "nice opportunity"
    },
    {
        "id" : 2, "company": "Ozon", "title" : "go backend",
        "url" : "https://ozon.ru/backend/go/internship", "status" : "test",
        "description" : "good company"
    },
    {
        "id" : 3, "company": "T-bank", "title" : "devops",
        "url" : "https://tbank.ru/devops/internship", "status" : "interview",
        "description" : "big company, devops is interesting"
    },
    {
        "id" : 4, "company": "Avito", "title" : "cyber security",
        "url" : "https://avito.ru/cybersec/internship", "status" : "rejected",
        "description" : "want to try"
    },
]

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/health")
async def health():
    return {"status" : "ok"}

@app.get("/api/v1/vacancies")
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

@app.get("/api/v1/vacancies/{vacancy_id}")
async def return_vacancy(vacancy_id:int):
    for vacancy in fake_db:
        if vacancy["id"] == vacancy_id:
            return vacancy
    raise HTTPException(
        status_code= 404,
        detail= "404. vacancy is not found"
    )

@app.get("/api/v1/stats")
async def vacancies_stats():
    vacancies = [Vacancy(**b) for b in fake_db]
    total = len(vacancies)
    total_by_status = {}
    for b in vacancies:
        total_by_status[b.status] = total_by_status.get(b.status, 0) + 1
    answer = {"total number of vacancies" : total, **total_by_status}
    return answer

@app.post("/api/v1/vacancies", response_model= VacancyRead, status_code=201)
async def create_vacancy(vacancy : VacancyCreate):
    vacancy_id = max((existing_vacancy["id"] for existing_vacancy in fake_db), default=0) + 1
    new_vacancy = {"id" : vacancy_id, **vacancy.model_dump()}
    fake_db.append(new_vacancy)
    return new_vacancy

@app.patch("/api/v1/vacancies/{vacancy_id}", status_code=200)
async def update_vacancy(new_data : VacancyUpdate, vacancy_id : int):
    if vacancy_id == None:
        raise HTTPException(status_code=400, detail="enter vacancy id")
    else:
        updates = new_data.model_dump(exclude_unset=True)
        for vacancy in fake_db:
            if vacancy["id"] == vacancy_id:
                for item in updates:
                    vacancy[item] = updates[item]
                    return vacancy
    raise HTTPException(status_code=404, detail="not found")

@app.delete("/api/v1/vacancies/{vacancy_id}", status_code=204)
async def delete_vacancy(vacancy_id : int):
    if vacancy_id == None:
        raise HTTPException(status_code=400, detail="enter vacancy id")
    else:
        for vacancy in fake_db:
            if vacancy["id"] == vacancy_id:
                fake_db.remove(vacancy)
                return
    raise HTTPException(status_code=404, detail="not found")
