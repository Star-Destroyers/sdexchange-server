from tortoise import fields
from tortoise.models import Model
from fastapi_users.db import TortoiseUserDatabase

from app.auth.schemas import UserDB
from app.auth.models import User

user_db = TortoiseUserDatabase(UserDB, User)


class TimestampMixin():
    created = fields.DatetimeField(null=True, auto_now_add=True)
    modified = fields.DatetimeField(null=True, auto_now=True)


class BaseModel(Model):
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True
