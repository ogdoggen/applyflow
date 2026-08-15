from fastapi import FastAPI
from .routes import vacancies, health, stats, tasks, auth


app = FastAPI()

app.include_router(vacancies.router)
app.include_router(health.router)
app.include_router(stats.router)
app.include_router(tasks.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

