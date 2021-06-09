from typing import List

from .models import Target
from .schema import TargetCreate, TargetUpdate


async def get_targets(limit: int = 100, offset: int = 0) -> List[Target]:
    targets = await Target.objects().limit(limit).offset(offset).run()
    return targets


async def create_target(target: TargetCreate) -> Target:
    t = Target(**target.dict())
    await t.save()
    return t


async def update_target(target: TargetUpdate) -> Target:
    t = await Target.objects().where(Target.id == target.id).first().run()
    for attr, val in target.dict(exclude_unset=True, exclude={'id'}).items():
        setattr(t, attr, val)
    await t.save()

    return t
