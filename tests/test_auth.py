import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_create_user(client : AsyncClient):
    create = await client.post("/auth/register", json={
                                                          "email": "test@user.com",
                                                          "password": "string"
                                                        })
    assert create.status_code == 201

    create2 = await client.post("/auth/register", json={
                                                          "email": "test@user.com",
                                                          "password": "string"
                                                        })
    assert create2.status_code == 409

    create3 = await client.post("/auth/register", json={
                                                            "email": "test2@user.com",
                                                            "password": "strin"
                                                        })
    assert create3.status_code == 422

    create4 = await client.post("/auth/register", json={
                                                            "email": "notvalid@email",
                                                            "password": "string"
                                                        })
    assert create4.status_code == 422
