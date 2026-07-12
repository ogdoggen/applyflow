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
|GET|/api/v1/stats| see vacancies statistics|
| POST | /api/v1/vacancies | create a new vacancy |
|PATCH| /api/v1/vacancies/{vacancy_id}| update a vacancy|
|DELETE| /api/v1/vacancies/{vacancy_id} | delete a vacancy|


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

## Update a vacancy

`PATCH /api/v1/vacancies/{vacancy_id}`

example of json:
```json
{
"status" : "interview",
"description" : "nice opportunity, I got interview tomorrow!"
}
```
You a free to write only updated parameters, there is no need to write the ones that are not changed.

## List all the vacancies

`GET /api/v1/vacancies`

available query parameters:
- status
- company
- limit

example:
`/api/v1/vacancies?status=test&company=ozon&limit=3`

## Possible errors
- 404 not found in http://127.0.0.1:8000/api/v1/vacancies/{vacancy_id} means {vacancy_id} you wrote is not found in database

