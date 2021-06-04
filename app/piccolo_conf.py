from piccolo.engine.postgres import PostgresEngine
from piccolo.conf.apps import AppRegistry

from app.config import settings

DB = PostgresEngine(
    config={
        'dsn': settings.DATABASE_URL
    }
)

APP_REGISTRY = AppRegistry(
    apps=['app.targets.piccolo_app', 'piccolo.apps.user.piccolo_app', 'app.auth.piccolo_app']
)
