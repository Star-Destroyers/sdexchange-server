from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from piccolo.engine import engine_finder

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


@app.get('/ping')
async def ping():
    return {'message': 'ok'}


@app.on_event("startup")
async def open_database_connection_pool():
    engine = engine_finder('app.piccolo_conf')
    if engine:
        await engine.start_connnection_pool(max_size=5)


@app.on_event("shutdown")
async def close_database_connection_pool():
    engine = engine_finder('app.piccolo_conf')
    if engine:
        await engine.close_connnection_pool()
