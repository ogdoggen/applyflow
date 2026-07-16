from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pygments.lexer import default

from app.schemas.vacancies import Vacancy, VacancyCreate, VacancyRead, VacancyUpdate, VacancyStatus

from .routes import vacancies, health, stats


app = FastAPI()

app.include_router(vacancies.router)
app.include_router(health.router)
app.include_router(stats.router)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

