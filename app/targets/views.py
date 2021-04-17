from app.targets.models import Target
from fastapi import APIRouter
from typing import List

from .schema import TargetSchema
from .crud import get_targets

router = APIRouter(
    prefix='/targets',
    tags=['target']
)

@router.get('/', response_model=List[TargetSchema])
async def targets(limit: int = 100, offset: int = 0):
    results = await get_targets(limit, offset)
    return results
