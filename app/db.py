from tortoise import fields
from tortoise.models import Model


class TimestampMixin():
    created = fields.DatetimeField(null=True, auto_now_add=True)
    modified = fields.DatetimeField(null=True, auto_now=True)


class BaseModel(Model):
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True
