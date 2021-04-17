from .models import Target

async def get_targets(limit: int = 100, offset: int = 0):
    targets = await Target.objects().limit(limit).offset(offset).run()
    return targets
