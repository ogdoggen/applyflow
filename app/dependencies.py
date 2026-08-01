from fastapi import Depends
from typing import Annotated
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

db_session = Annotated[AsyncSession, Depends(get_db)]