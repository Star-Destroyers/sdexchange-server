from pydantic import BaseModel
from datetime import datetime
from typing import Optional


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

class TargetSchema(TargetBase):
    id: int
    created: datetime

    class Config:
        orm_mode = True


class Detection(BaseModel):
    target: TargetSchema
    candid: int
    filter: str
    magpsf: float
    sigmapsf: float
    diffmaglim: float
    isdiffpos: str
    jd: float
    utc: datetime
    created: datetime

    class Config:
        orm_mode = True
