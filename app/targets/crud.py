from typing import List

from .models import Target
from .schema import TargetCreate, TargetUpdate


async def get_targets(limit: int = 100, offset: int = 0) -> List[Target]:
    targets = await Target.all().limit(limit).offset(offset)
    return targets


async def create_target(target: TargetCreate) -> Target:
    t = await Target.create(**target.dict())
    return t


async def update_target(target: TargetUpdate) -> Target:
    t = await Target.get(pk=target.id)
    for attr, val in target.dict(exclude_unset=True, exclude={'id'}).items():
        setattr(t, attr, val)
    await t.save()

    return t
