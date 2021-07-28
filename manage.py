from IPython import embed
import nest_asyncio
from app.config import settings
from tortoise import Tortoise
import asyncio


async def main():
    banner = 'Additional imports:\n'
    from app.main import app
    banner = banner + 'from app.main import app\n'
    await Tortoise.init(db_url=settings.DATABASE_URL, modules=settings.TORTOISE['modules'])
    for name, model in Tortoise.apps['models'].items():
        globals()[name] = model
        banner = banner + f'from {model.__module__} import {model.__name__}\n'
    nest_asyncio.apply()
    embed(colors='neutral', using='asyncio', banner2=banner)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
