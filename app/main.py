from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pygments.lexer import default

from app.schemas.vacancies import VacancyCreate, VacancyRead

vacancies = ["python backend", "go backend", "devops", "cyber security"]
fake_db = [
    {"id" : 1, "company": "Yandex", "title" : "python backend", "url" : "yandex.ru/backend/internship", "status" : "applied", "description" : "nice opportunity"},
    {"id" : 2, "company": "Ozon", "title" : "go backend", "url" : "ozon.ru/backend/go/internship", "status" : "test", "description" : "good company"},
    {"id" : 3, "company": "T-bank", "title" : "devops", "url" : "tbank.ru/devops/internship", "status" : "interview", "description" : "big company, devops is interesting"},
    {"id" : 4, "company": "Avito", "title" : "cyber security", "url" : "avito.ru/cybersec/internship", "status" : "rejected", "description" : "want to try"},
]

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/health")
async def health():
    return {"status" : "ok"}

@app.get("/api/v1/vacancies")
async def write_vacancies():
    return fake_db

@app.get("/api/v1/vacancies/{vacancy_id}")
async def return_vacancy(vacancy_id:int):
    for vacancy in fake_db:
        if vacancy["id"] == vacancy_id:
            return vacancy
    raise HTTPException(
        status_code= 404,
        detail= "404. vacancy is not found"
    )

@app.post("/api/v1/vacancies", response_model= VacancyRead, status_code=201)
async def create_vacancy(vacancy : VacancyCreate):
    vacancy_id = max((existing_vacancy["id"] for existing_vacancy in fake_db), default=0) + 1
    new_vacancy = {"id" : vacancy_id, **vacancy.model_dump()}
    fake_db.append(new_vacancy)

    return new_vacancy