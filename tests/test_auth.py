import pytest
from httpx import AsyncClient

#------------------
#reusable functions
async def register_user(client : AsyncClient, email : str = "test@email.com", password : str = "password"):
    user = await client.post("/auth/register", json={
                                                          "email": email,
                                                          "password": password
                                                        })
    return user

async def login_user(client : AsyncClient, email : str, password : str):
    login = await client.post("/auth/login",
                              data = {
                                  "username" : email,
                                  "password" : password,
                              })
    return login

async def get_auth_token(client : AsyncClient, email : str, password : str):
    await register_user(client, email, password)
    user = await login_user(client, email, password)
    token = user.json()["access_token"]
    return {"Authorization" : f"Bearer {token}"}


#------------------

#test functions
@pytest.mark.anyio
async def test_register_user(client : AsyncClient):
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

@pytest.mark.anyio
async def test_login_user(client : AsyncClient):
    user = await register_user(client, "test@user2.com", "password")

    correct = await login_user(client, "test@user2.com", "password")
    assert correct.status_code == 200

    wrong_password = await login_user(client, "test@user2.com", "wrong_password")
    assert wrong_password.status_code == 401

    wrong_email = await login_user(client, "wrong@email.com", "password")
    assert wrong_email.status_code == 401