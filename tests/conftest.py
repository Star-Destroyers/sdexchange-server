from pydantic.env_settings import BaseSettings
from app.auth.security import get_current_active_user
from typing import Generator
import pytest
from asyncio import get_event_loop
from httpx import AsyncClient
from piccolo.apps.migrations.commands.forwards import run_forwards
from piccolo.apps.migrations.commands.backwards import run_backwards
from piccolo.apps.user.tables import BaseUser

from app.main import app


@pytest.fixture(scope='session')
def event_loop():
    event_loop = get_event_loop()
    yield event_loop
    event_loop.close()

@pytest.fixture(scope='session', autouse=True)
async def run_migrations():
    print('Running Migrations')
    await run_forwards(app_name='all')

    yield

    print('Reversing Migrations')
    await run_backwards(app_name='all', migration_id=0, auto_agree=True)

@pytest.fixture(scope='module')
async def client() -> Generator:
    async with AsyncClient(app=app, base_url='http://127.0.0.1') as client:
        yield client

@pytest.fixture
async def basic_user() -> BaseUser:
    base_user = BaseUser(
        username='basic_user',
        password='test123',
        email='test@example.com',
        first_name='Fabius',
        last_name='Teevult',
        active=True,
        admin=False,
        superuser=False
    )
    await base_user.save()
    app.dependency_overrides[get_current_active_user] = lambda: base_user
    yield base_user
    app.dependency_overrides = {}
    await BaseUser.delete().where(BaseUser.id == base_user.id)
