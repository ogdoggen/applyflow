# ApplyFlow
ApplyFlow is a simple program for tracking internship applications.

# Features
- view all vacancies
- view a vacancy by id
- create a new vacancy
- automatic request validation
- automatic documentation

## Run locally:
Make sure dependencies are installed:

```bash
python -m pip install -r requirements.txt
```

```bash
python -m uvicorn app.main:app --reload
```

## Available Endpoints


| Method | Endpoint | Description |
|---|---|---|
| GET | / | root |
| GET | /health | health check |
| GET | /api/v1/vacancies | see all vacancies |
| GET | /api/v1/vacancies/{vacancy_id} | see a vacancy by id |
| POST | /api/v1/vacancies | create a new vacancy |

## API documentation

- API docs: http://127.0.0.1:8000/docs
- alternative API docs: http://127.0.0.1:8000/redoc

## Create a vacancy

`POST /api/v1/vacancies`
example of json:
```json
{
"company": "Yandex",
"title" : "python backend",
"url" : "yandex.ru/backend/internship",
"status" : "applied",
"description" : "nice opportunity"
}
```

## Possible errors
- 404 not found in http://127.0.0.1:8000/api/v1/vacancies/{vacancy_id} means {vacancy_id} you wrote is not found in database

