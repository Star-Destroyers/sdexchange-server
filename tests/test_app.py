from fastapi.testclient import TestClient
from fastapi import status

from app.main import app

client = TestClient(app)


class TestMain:
    def test_ping(self):
        response = client.get(app.url_path_for('ping'))
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['message'] == 'ok'
