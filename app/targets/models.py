from piccolo.table import Table
from piccolo.columns import Varchar, Timestamp, Real, BigInt, ForeignKey
from datetime import datetime, timedelta
from typing import List


class Target(Table):
    name: str = Varchar(index=True, required=True, unique=True)
    classification: str = Varchar(requird=False, default='')
    ra: float = Real(required=True)
    dec: float = Real(required=True)
    utc: datetime = Timestamp(required=True)
    latest_r_mag: float = Real(null=True, default=None)
    latest_g_mag: float = Real(null=True, default=None)
    max_r_mag: float = Real(null=True, default=None)
    max_g_mag: float = Real(null=True, default=None)
    created: datetime = Timestamp()
    sparkline: List[float] = []

    async def fetch_sparkline(self) -> List[float]:
        detections: List[dict[float, datetime]] = await Detection.select(
            Detection.magpsf, Detection.utc
        ).where(
            (Detection.target == self.id) & (Detection.utc >= datetime.utcnow() - timedelta(days=30))
        ).order_by(Detection.utc)

        days = [None] * 32
        for detection in detections:
            days[detection['utc'].day] = detection['magpsf']

        self.sparkline = days


class Detection(Table):
    target: Target = ForeignKey(Target)
    candid: int = BigInt(required=True, index=True, unique=True)
    filter: str = Varchar(required=True)
    magpsf: float = Real(required=True)
    sigmapsf: float = Real(required=True)
    diffmaglim: float = Real(required=True)
    isdiffpos: str = Varchar(length=1, required=True)
    jd: float = Real(required=True)
    utc: datetime = Timestamp(required=True)
    created: datetime = Timestamp()
