# ApplyFlow
ApplyFlow is a simple program for tracking internships applications.

## Run locally:
Make sure dependencies are installed:

```bash
python -m pip install -r requirements.txt
```

```bash
python -m uvicorn app.main:app --reload
```

## Endpoints
- Root: http://127.0.0.1:8000 
- Health: http://127.0.0.1:8000/health 
- API docs: http://127.0.0.1:8000/docs 
- All vacancies: http://127.0.0.1:8000/api/v1/vacancies
- Vacancy with id {vacancy_id}: http://127.0.0.1:8000/api/v1/vacancies/{vacancy_id}

## Possible errors
- 404 not found in http://127.0.0.1:8000/api/v1/vacancies/{vacancy_id} means {vacancy_id} you wrote is not found in database

