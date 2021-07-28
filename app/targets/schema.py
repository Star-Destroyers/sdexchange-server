from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Union


class TargetBase(BaseModel):
    name: str
    classification: str
    ra: float
    dec: float
    utc: datetime
    latest_r_mag: Optional[float]
    latest_g_mag: Optional[float]
    max_r_mag: Optional[float]
    max_g_mag: Optional[float]


class TargetCreate(TargetBase):
    pass


class TargetUpdate(TargetBase):
    id: int
    name: Optional[str]
    classification: Optional[str]
    ra: Optional[float]
    dec: Optional[float]
    utc: Optional[datetime]


class TargetDetail(TargetBase):
    id: int
    created: datetime
    sparkline: Optional[List[Union[float, None]]]

    class Config:
        orm_mode = True


class Detection(BaseModel):
    target_id: int
    candid: int
    filter_id: str
    magpsf: float
    sigmapsf: float
    diffmaglim: float
    isdiffpos: str
    jd: float
    utc: datetime
    created: datetime

    class Config:
        orm_mode = True
