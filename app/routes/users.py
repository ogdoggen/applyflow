from fastapi import APIRouter

from app.dependencies import CurrentUser
from app.schemas.users import UserRead

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get("/me", response_model=UserRead)
async def get_me(current_user: CurrentUser):
    return current_user