from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.schemas.users import UserRead, UserCreate
from app.dependencies import db_session
from app.schemas.token import Token

from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserRead, status_code=201)
async def create_user(session : db_session, user : UserCreate):
    return await auth_service.create_user(session, user)

@router.post("/login", response_model=Token)
async def login(session : db_session,
                form_data : Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await auth_service.login(session, form_data)





