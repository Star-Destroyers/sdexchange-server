from fastapi import FastAPI
from app.explorer.views import router as explorer_router
from fastapi.middleware.cors import CORSMiddleware
from piccolo.engine import engine_finder
import os

from app.config import settings

app = FastAPI(title=settings.APP_NAME)
app.include_router(explorer_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get('/ping')
async def ping():
    return {'message': 'ok'}

@app.on_event("startup")
async def open_database_connection_pool():
    engine = engine_finder('app.piccolo_conf')
    await engine.start_connnection_pool()


@app.on_event("shutdown")
async def close_database_connection_pool():
    engine = engine_finder('app.piccolo_conf')
    await engine.close_connnection_pool()
