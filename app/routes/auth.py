from fastapi import APIRouter

from app.schemas.users import UserRead, UserCreate
from app.dependencies import db_session

from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserRead, status_code=201)
async def create_user(session : db_session, user : UserCreate):
    return await auth_service.create_user(session, user)


