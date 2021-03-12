from fastapi import FastAPI

from app.explorer.views import router as explorer_router
from fastapi.middleware.cors import CORSMiddleware

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

