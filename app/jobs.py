from arq.connections import RedisSettings
from arq import cron
import logging

from app.targets.ingest import ingest

logger = logging.getLogger(__name__)


async def test_job(ctx):
    print('Test job!')


async def get_latest_alerts(ctx) -> None:
    await ingest()


class WorkerSettings:
    redis_settings = RedisSettings()
    cron_jobs = [
        cron(test_job, hour=None, minute=None, second=None)
    ]
