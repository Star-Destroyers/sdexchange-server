from typing import Generator
import pytest
from asyncio import get_event_loop
from httpx import AsyncClient
from app.auth.models import User
from tortoise.contrib.test import finalizer, initializer

from app.main import app
from app.config import settings
from app.auth.schemas import UserCreate, UserDB


@pytest.fixture(scope='session')
def event_loop():
    event_loop = get_event_loop()
    yield event_loop
    event_loop.close()


@pytest.fixture(scope='module')
async def client() -> Generator:
    async with AsyncClient(app=app, base_url='http://127.0.0.1') as client:
        yield client


@pytest.fixture(scope='session', autouse=True)
def initialize_tests(request):
    initializer(
        settings.TORTOISE['modules']['models'],
        db_url="sqlite://./test_db.sqlite3",
        app_label="test_app"
    )
    request.addfinalizer(finalizer)


@pytest.fixture
async def basic_user() -> UserDB:
    user_create = UserCreate(
        username='test_user',
        password='test123',
        email='test@example.com',
        is_active=True,
        is_superuser=False,
        is_verified=True
    )

    user = await fastapi_users.create_user(user_create)
    # app.dependency_overrides[app.fastapi_users.current_user] = lambda: user
    yield user
    app.dependency_overrides = {}
    await User.filter(id=user.id).delete()
