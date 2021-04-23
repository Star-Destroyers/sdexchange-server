from fastapi.testclient import TestClient
from fastapi import status
from datetime import datetime
from httpx import AsyncClient
import pytest

from app.main import app
from app.targets.models import Target
from app.targets.crud import create_target
from app.targets.schema import TargetCreate

client = TestClient(app)

class TestTargets:
    @pytest.mark.asyncio
    async def test_list_targets(self, client: AsyncClient) -> None:
        tc = TargetCreate(
            name='ZTFTestTarget',
            classification='NT',
            ra=42.2,
            dec=41.2,
            utc=datetime.utcnow(),
            latest_r_mag=23,
            latest_g_mag=66,
            max_r_mag=54,
            max_g_mag=87
        )
        target = await create_target(tc)
        print(target)

        response = await client.get(app.url_path_for('targets'))
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]['id'] == target.id

