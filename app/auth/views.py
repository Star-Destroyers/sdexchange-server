from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from piccolo.apps.user.tables import BaseUser
from datetime import timedelta

from app.config import settings
from . import schemas, crud
from .security import create_access_token, get_current_active_user, verify_password


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/token', response_model=schemas.Token)
async def token(form: OAuth2PasswordRequestForm = Depends()):
    user_id = await BaseUser.login(form.username, form.password)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    user: BaseUser = await crud.get_user(user_id)
    access_token_expires = timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.email}, expires_delta=access_token_expires
    )

    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.get('/users/me', response_model=schemas.UserDetail)
async def me(current_user: BaseUser = Depends(get_current_active_user)):
    return current_user


@router.patch('/users/me', response_model=schemas.UserDetail)
async def update_user_me(
    update_user: schemas.UserUpdate,
    current_user: BaseUser = Depends(get_current_active_user),
):
    user = await crud.update_user(update_user, current_user.id)

    return user


@router.post('users/me/update_password')
async def update_password_me(
    password_update: schemas.PasswordUpdate,
    current_user: BaseUser = Depends(get_current_active_user)
):
    if not verify_password(current_user, password_update.current_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect password',
        )
    else:
        await BaseUser.update_password(current_user.id, password_update.password)

    return {'detail': 'ok'}
