from piccolo.apps.user.tables import BaseUser
from . import schemas


async def get_user(user_id: int) -> BaseUser:
    return await BaseUser.objects().where(BaseUser.id == user_id).first()


async def update_user(update_user: schemas.UserUpdate, user_id: int) -> BaseUser:
    user = await get_user(user_id)
    update_data = update_user.dict(exclude_unset=True)
    for k, v in update_data.items():
        setattr(user, k, v)
    await user.save()

    return user
