import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_create_read_vacancy(client : AsyncClient):
    create_response = await client.post("/vacancies",
                                 json= {
                                  "company": "Test Company",
                                  "title": "test title",
                                  "url": "https://example.com/test",
                                  "status": "saved",
                                  "description": "test_test_test"
                                })

    assert create_response.status_code == 201

    vacancy_id = create_response.json()["id"]
    read_response = await client.get(f"/vacancies/{vacancy_id}")

    assert read_response.status_code == 200
    assert read_response.json() == {
                                  "id":vacancy_id,
                                  "company": "Test Company",
                                  "title": "test title",
                                  "url": "https://example.com/test",
                                  "status": "saved",
                                  "description": "test_test_test"
                                }

@pytest.mark.anyio
async def test_422_in_create_vacancy(client: AsyncClient):
    create_response = await client.post("/vacancies",
                           json={
                               "company": "Test Company",

                               "url": "https://example.com/test",
                               "status": "saved",
                               "description": "test_test_test"
                           })
    assert create_response.status_code == 422

@pytest.mark.anyio
async def test_404_in_create_vacancy(client : AsyncClient):
    create_response = await client.get(f"/vacancies/{999999}")
    assert create_response.status_code == 404

@pytest.mark.anyio
async def test_patch_undefined_fields(client : AsyncClient):
    create_response = await client.post("/vacancies",
                                 json={
                                     "company": "Test Company",
                                     "title": "unchanged title",
                                     "url": "https://example.com/test",
                                     "status": "saved",
                                     "description": "test_test_test"
                                 })


    title = create_response.json()["title"]
    id = create_response.json()["id"]

    patch_response = await client.patch(f"/vacancies/{id}",
                                  json={
                                      "company": "changed"
                                  })
    assert patch_response.json()["title"] == title