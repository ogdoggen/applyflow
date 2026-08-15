from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from pydantic import EmailStr

from app.models.user import UserModel
from app.schemas.users import UserCreate

from app.security import hash_password


async def get_user_by_email(session : AsyncSession, email : EmailStr):
    stmt = select(UserModel).where(UserModel.email == email)
    result = await session.scalar(stmt)
    if result is None:
        raise HTTPException(status_code=404, detail="email not found")
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
