from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from pydantic import EmailStr
from typing import Annotated

from app.models.user import UserModel
from app.schemas.users import UserCreate
from app.schemas.token import Token

from app.security import hash_password, verify_password, create_access_token


async def get_user_by_email(session : AsyncSession, email : EmailStr):
    stmt = select(UserModel).where(UserModel.email == email)
    result = await session.scalar(stmt)
    # if result is None:
    #     raise HTTPException(status_code=404, detail="email not found")
    return result

async def check_email_exists_error(session : AsyncSession, email : EmailStr):
    stmt = select(UserModel).where(UserModel.email == email)
    result = await session.scalar(stmt)
    if result is not None:
        raise HTTPException(status_code=409, detail="such email already exists")


async def create_user(session : AsyncSession, user : UserCreate):
    password_hash = hash_password(user.password)
    await check_email_exists_error(session, user.email)
    new_user = UserModel(email = user.email, password_hash = password_hash)
    session.add(new_user)
    try:
        await session.commit()
        await session.refresh(new_user)
    except:
        await session.rollback()
        raise
    return new_user

async def login(session : AsyncSession,
                form_data : Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await get_user_by_email(session, form_data.username)
    if user is None:
        raise HTTPException(status_code=401, detail="incorrect email or password")
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="incorrect email or password")
    access_token = create_access_token(user.id)
    return Token(access_token=access_token, token_type="bearer")