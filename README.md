# ApplyFlow
ApplyFlow is a simple program for tracking internship applications.

## Features
- view all vacancies
- view a vacancy by id
- create a new vacancy
- create/update/delete preparation tasks for vacancy
- automatic request validation
- automatic documentation

## Tech Stack

- Python 3.14
- FastAPI
- Pydantic
- Uvicorn
- PostgreSQL 17
- Docker
- Docker Compose
- Git

## Project structure

```text
.
├── app
│   ├── main.py
│   ├── config.py
│   ├── fake_database.py
│   ├── routes
│   │   ├── health.py
│   │   ├── vacancies.py
│   │   ├── tasks.py
│   │   └── stats.py
│   ├── schemas
│   │   ├── vacancy.py
│   │   └── task.py
│   └── services
        ├── stats_service.py
│       ├── vacancy_service.py
│       └── task_service.py
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Available Endpoints


| Method | Endpoint                                | Description |
|-----|-----------------------------------------|---|
| GET | /                                       | root |
| GET | /health                                 | health check |
| GET | /vacancies                              | see all vacancies |
| GET | /vacancies/{vacancy_id}                 | see a vacancy by id |
| GET | /stats                                  | see vacancies statistics|
| POST | /vacancies                              | create a new vacancy |
| PATCH | /vacancies/{vacancy_id}                 | update a vacancy|
| DELETE | /vacancies/{vacancy_id}                 | delete a vacancy|
| GET | /vacancies/{vacancy_id}/tasks           | Get tasks for a vacancy |
| POST | /vacancies/{vacancy_id}/tasks           | Create a task for a vacancy |
|DELETE | /vacancies/{vacancy_id}/tasks/{task_id} | Delete prep task|


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

## Running the project with Docker Compose

### Prerequisites

Install:

- Docker
- Docker Compose
- Git

Docker Compose is included with current versions of Docker Desktop.

### 1. Clone the repository

```bash
git clone https://github.com/ogdoggen/applyflow
cd fast_api_first_touch
```

### 2. Create the environment file

Copy the example file:

```bash
cp .env.example .env
```

### 3. Build and start the services

Run the containers in the foreground:

```bash
docker compose up --build
```

### 4. Connect to PostgreSQL

```bash
docker compose exec db \
  psql -U applyflow_user -d applyflow
```

### 5. Stop the project

```bash
docker compose down
```

### 6. Completely reset PostgreSQL

```bash
docker compose down -v
```
