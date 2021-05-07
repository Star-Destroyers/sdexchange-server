from fastapi import APIRouter
from typing import List

from sd_alert_pipe.lasair import LasairService
from sd_alert_pipe.common import RootResult, gather_data
from sd_alert_pipe.tns import TNSService

router = APIRouter(
    prefix='/explorer',
    tags=['explorer']
)

@router.get('/lasair_query/')
async def lasair_query(query_id: str) -> dict:
    ls = LasairService()
    result = await ls.stored_query(query_id)
    return result

@router.get('/ztfobject/{object_id}/', response_model=RootResult)
async def ztfobject(object_id: str) -> RootResult:
    result = await gather_data(object_id)
    return result

@router.get('/tns/cone/')
async def tnscode(ra: float, dec: float) -> List[dict]:
    tns = TNSService()
    result = await tns.cone_search(ra, dec)
    return result

@router.get('/tns/detail/{objname}/')
async def tnsdetail(objname: str) -> dict:
    tns = TNSService()
    result = await tns.get_tns_object(objname)
    return result
