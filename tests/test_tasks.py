import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_create_task_without_vacancy(client : AsyncClient):
    response = await client.post(f"/vacancies/{9999}/tasks",
                                 json={
                                          "title": "test task",
                                          "notes": "test notes",
                                          "due_date": "2026-08-09"
                                        })
    assert response.status_code == 404

@pytest.mark.anyio
async def test_create_list_task(client : AsyncClient):
    create_vacancy_response = await client.post("/vacancies",
                                                json={
                                              "company": "Test Company",
                                              "title": "test create and list task",
                                              "url": "https://example.com/",
                                              "status": "saved",
                                              "description": "string"
                                            })
    assert create_vacancy_response.status_code == 201
    vacancy_id = create_vacancy_response.json()["id"]

    create_response = await client.post(f"/vacancies/{vacancy_id}/tasks",
                                        json={
                                                "title": "create task",
                                                "notes": "test notes",
                                                "due_date": "2026-08-09"
                                            })
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    list_response = await client.get(f"/vacancies/{vacancy_id}/tasks/{task_id}")
    assert list_response.status_code == 200
    assert list_response.json() == {
                                        "id":task_id,
                                        "vacancy_id":vacancy_id,
                                        "title": "create task",
                                        "notes": "test notes",
                                        "is_done": False,
                                        "due_date": "2026-08-09"
                                    }

@pytest.mark.anyio
async def test_get_not_your_task(client : AsyncClient):
    create_vacancy = await client.post("/vacancies",
                                                        json={
                                                          "company": "test1",
                                                          "title": "string",
                                                          "url": "https://example.com/",
                                                          "status": "saved",
                                                          "description": "string"
                                                        })
    vacancy_id = create_vacancy.json()["id"]

    create_another_vacancy = await client.post("/vacancies",
                                               json={
                                                   "company": "test2",
                                                   "title": "string",
                                                   "url": "https://example.com/",
                                                   "status": "saved",
                                                   "description": "string"
                                               })

    another_vacancy_id = create_another_vacancy.json()["id"]

    create_task = await client.post(f"/vacancies/{vacancy_id}/tasks",
                                    json={
                                          "title": "string",
                                          "notes": "string",
                                          "due_date": "2026-08-12"
                                        })
    task_id = create_task.json()["id"]

    get_task = await client.get(f"/vacancies/{another_vacancy_id}/tasks/{task_id}")
    assert get_task.status_code == 404


