from typing import Generator
import pytest
from asyncio import get_event_loop
from httpx import AsyncClient
from piccolo.apps.migrations.commands.forwards import forwards
from piccolo.apps.migrations.commands.backwards import backwards

from app.main import app


@pytest.fixture(scope='session')
def event_loop():
    event_loop = get_event_loop()
    yield event_loop
    event_loop.close()

@pytest.fixture(scope='session', autouse=True)
async def run_migrations():
    try:
        print('Running Migrations')
        await forwards(app_name='all')
    except SystemExit:
        pass

    yield

    try:
        print('Reversing Migrations')
        await backwards(app_name='all', migration_id=0, auto_agree=True)
    except SystemExit:
        pass

@pytest.fixture(scope='module')
async def client() -> Generator:
    async with AsyncClient(app=app, base_url='http://127.0.0.1') as client:
        yield client
