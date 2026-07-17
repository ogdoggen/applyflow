
from ..fake_database import fake_vacancies_db
from app.schemas.vacancies import Vacancy

async def vacancies_stats():
    vacancies = [Vacancy(**b) for b in fake_vacancies_db]
    total = len(vacancies)
    total_by_status = {}
    for b in vacancies:
        total_by_status[b.status] = total_by_status.get(b.status, 0) + 1
    answer = {"total number of vacancies" : total, **total_by_status}
    return answer