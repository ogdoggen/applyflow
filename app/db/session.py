from app.config import settings
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

engine = create_async_engine(settings.database_url, pool_pre_ping = True, echo = settings.debug)

session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
async def get_db():
    db = session_factory()
    try:
        yield db
    finally:
        await db.close()
