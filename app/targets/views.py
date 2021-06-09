from fastapi import APIRouter
from typing import List

from .schema import TargetDetail
from .crud import get_targets

router = APIRouter(
    prefix='/targets',
    tags=['target']
)


@router.get('/', response_model=List[TargetDetail])
async def targets(limit: int = 100, offset: int = 0):
    results = await get_targets(limit, offset)
    for target in results:
        await target.fetch_sparkline()

    return results
