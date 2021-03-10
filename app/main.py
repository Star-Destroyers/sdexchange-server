from fastapi import FastAPI

from app.explorer.views import router as explorer_router
from app.config import settings

app = FastAPI(title=settings.APP_NAME)
app.include_router(explorer_router)

@app.get('/ping')
async def ping():
    return {'message': 'ok'}

