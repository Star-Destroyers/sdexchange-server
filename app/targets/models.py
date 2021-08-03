from tortoise import fields
from datetime import datetime, timedelta
from typing import List, Optional

from app.db import TimestampMixin, BaseModel


class Target(TimestampMixin, BaseModel):
    name: str = fields.CharField(max_length=200, index=True, unique=True)
    classification: str = fields.CharField(max_length=200, default='')
    ra: float = fields.FloatField()
    dec: float = fields.FloatField()
    utc: datetime = fields.DatetimeField()
    latest_r_mag: float = fields.FloatField(null=True, default=None)
    latest_g_mag: float = fields.FloatField(null=True, default=None)
    max_r_mag: float = fields.FloatField(null=True, default=None)
    max_g_mag: float = fields.FloatField(null=True, default=None)
    detections: fields.ReverseRelation['Detection']
    sparkline: List[Optional[float]] = []

    class Meta:
        app = 'Targets'

    async def fetch_sparkline(self):
        detections: List[dict[float, datetime]] = await self.detections.filter(
            utc__gte=datetime.utcnow() - timedelta(days=30)
        ).order_by('utc').values('magpsf', 'utc')

        days = [None] * 32
        for detection in detections:
            days[detection['utc'].day] = detection['magpsf']

        self.sparkline = days


class Detection(TimestampMixin, BaseModel):
    target: fields.ForeignKeyRelation[Target] = fields.ForeignKeyField('Targets.Target', on_delete=fields.CASCADE, related_name='detections')
    candid: int = fields.BigIntField(index=True, unique=True)
    filter_id: str = fields.CharField(max_length=20)
    magpsf: float = fields.FloatField()
    sigmapsf: float = fields.FloatField()
    diffmaglim: float = fields.FloatField()
    isdiffpos: str = fields.CharField(max_length=1)
    jd: float = fields.FloatField()
    utc: datetime = fields.DatetimeField()
    created: datetime = fields.DatetimeField(auto_now_add=True)
    modified: datetime = fields.DatetimeField(auto_now=True)

    class Meta:

        app = 'Targets'
