from fastapi import Depends, HTTPException
from typing import Annotated
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserModel
from app.security import decode_access_token, oauth2_scheme




db_session = Annotated[AsyncSession, Depends(get_db)]



async def get_current_user(session : db_session, token : Annotated[str, Depends(oauth2_scheme)]):
    user_id = decode_access_token(token)
    user = await session.get(UserModel, int(user_id))
    if user is None:
        raise HTTPException(status_code=401, detail="unauthorized")
    return user

CurrentUser = Annotated[
    UserModel,
    Depends(get_current_user),
]