from fastapi import status
from httpx import AsyncClient
from app.auth.models import User
from app.auth.schemas import UserCreate
import pytest

from app.main import app, fastapi_users


class TestAuth:
    @pytest.mark.asyncio
    async def test_login(self, client: AsyncClient) -> None:
        creds = {'username': 'testagain@example.com', 'password': 'abc123'}
        await fastapi_users.create_user(UserCreate(email=creds['username'], password=creds['password']))

        response = await client.post(app.url_path_for('login'), data=creds)
        print(response.content)
        assert response.status_code == status.HTTP_200_OK
        assert 'access_token' in response.json()

    @pytest.mark.asyncio
    async def test_me(self, client: AsyncClient, basic_user: User) -> None:
        response = await client.get(app.url_path_for('me'))
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['email'] == basic_user.email

    @pytest.mark.asyncio
    async def test_me_not_logged_in(self, client: AsyncClient) -> None:
        response = await client.get(app.url_path_for('me'))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_protected_route(self, client: AsyncClient, basic_user: User) -> None:
        response = await client.get(app.url_path_for('protected_route'))
        print(response.content)
        assert response.status_code == status.HTTP_200_OK
