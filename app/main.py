from fastapi import FastAPI, HTTPException

vacancies = ["python backend", "go backend", "devops", "cyber security"]
fake_db = {
    1 : {"id" : 1, "company": "Yandex", "vacancy" : "python backend"},
    2 : {"id" : 2, "company": "Ozon", "vacancy" : "go backend"},
    3 : {"id" : 3, "company": "T-bank", "vacancy" : "devops"},
    4 : {"id" : 4, "company": "Avito", "vacancy" : "cyber security"},
}

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/health")
async def health():
    return {"status" : "ok"}

@app.get("/api/v1/vacancies")
async def write_vacancies():
    return list(fake_db.values())

@app.get("/api/v1/vacancies/{vacancy_id}")
async def return_vacancy(vacancy_id:int):
    vacancy = fake_db.get(vacancy_id)
    if vacancy == None:
        raise HTTPException(
            status_code = 404,
            detail = "404 Item not found"
        )
    return vacancy
