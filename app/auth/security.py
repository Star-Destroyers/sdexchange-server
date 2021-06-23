from typing import Optional
from datetime import timedelta, datetime
from jose import JWTError, jwt
from app.config import settings
from piccolo.apps.user.tables import BaseUser
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from . import schemas

JWT_ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, JWT_ALGORITHM)

    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> BaseUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate':  'Bearer'},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get('sub', '')
        if not username:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = await BaseUser.objects().where(BaseUser.username == token_data.username).first()
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: BaseUser = Depends(get_current_user)) -> BaseUser:
    if not current_user.active:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user


def verify_password(user: BaseUser, password: str) -> bool:
    _, iterations, salt, _ = BaseUser.split_stored_password(user.password)
    return BaseUser.hash_password(password, salt, int(iterations)) == user.password
