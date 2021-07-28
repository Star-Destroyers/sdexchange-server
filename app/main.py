from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib import fastapi
import logging

from app.config import settings
from app.explorer.views import router as explorer_router
from app.targets.views import router as target_router
from app.auth.views import router as auth_rotuer

app = FastAPI(title=settings.APP_NAME)
app.include_router(explorer_router)
app.include_router(target_router)
app.include_router(auth_rotuer)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

fastapi.logging = logging.getLogger('uvicorn')
fastapi.register_tortoise(
    app=app,
    db_url=settings.DATABASE_URL,
    modules=settings.TORTOISE['modules'],
    generate_schemas=True,
    add_exception_handlers=True
)


@app.get('/ping')
async def ping():
    return {'message': 'ok'}
