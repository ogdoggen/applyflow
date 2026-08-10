import pytest

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings

from app.db.base import Base
import app.models

from httpx import ASGITransport, AsyncClient

from app.main import app
from app.db.session import get_db

test_engine = create_async_engine(settings.test_database_url)
test_session_factory = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False
)

async def override_get_db():
    test_db = test_session_factory()
    try:
        yield test_db
    finally:
        await test_db.close()

@pytest.fixture(scope="session")
def anyio_backend(): return "asyncio"

@pytest.fixture(scope="session", autouse=True)
async def prepare_test_database(anyio_backend):
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()

@pytest.fixture
async def client():
    app.dependency_overrides[get_db()] = override_get_db()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()