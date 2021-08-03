from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib import fastapi
from fastapi_users import FastAPIUsers
import logging

from app.config import settings
from app.db import user_db
from app.auth.security import auth_backends, jwt_authentication
from app.auth.schemas import User, UserDB, UserCreate, UserUpdate
from app.explorer.views import router as explorer_router
from app.targets.views import router as target_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)
    return app


app = create_app()

fastapi.logging = logging.getLogger('uvicorn')

fastapi.register_tortoise(
    app=app,
    db_url=settings.DATABASE_URL,
    modules=settings.TORTOISE['modules'],
    generate_schemas=True,
    add_exception_handlers=True
)

fastapi_users = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB
)

app.include_router(explorer_router)
app.include_router(target_router)
app.include_router(
    fastapi_users.get_auth_router(jwt_authentication),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(settings.SECRET_KEY),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(),
    prefix="/users",
    tags=["users"],
)

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


@app.get("/protected-route")
def protected_route(user: User = Depends(fastapi_users.current_user())):
    return f"Hello, {user.email}"
