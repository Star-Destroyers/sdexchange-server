from fastapi import APIRouter
from sd_alert_pipe.lasair import LasairService
from sd_alert_pipe.common import gather_data

router = APIRouter(
    prefix='/explorer',
    tags=['explorer']
)

@router.get('/lasair_query/')
async def lasair_query(query_id: str) -> dict:
    ls = LasairService()
    result = await ls.stored_query(query_id)
    return result

@router.get('/ztfobject/{object_id}/')
async def ztfobject(object_id: str) -> dict:
    result = await gather_data(object_id)
    return {**result.dict()}

