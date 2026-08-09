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
