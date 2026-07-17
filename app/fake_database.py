from datetime import date

fake_vacancies_db = [
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

fake_tasks_db = [
    {
        "id" : 1, "vacancy_id" : 1, "title" : "leetcode tasks",
        "notes" : "look for top 20 yandex interview tasks and solve it",
        "is_done" : False, "due_date" : date(2026, 7, 25)
    },
{
        "id" : 2, "vacancy_id" : 1, "title" : ",ost common questions",
        "notes" : "look for most popular questions on Yandex interviews and prepare for them",
        "is_done" : False, "due_date" : date(2026, 7, 27)
    },
{
        "id" : 3, "vacancy_id" : 1, "title" : "github prep",
        "notes" : "look at your github repos, make good ones public, hide bad ones, set bio, profile photo",
        "is_done" : False, "due_date" : date(2026, 7, 28)
    }
]