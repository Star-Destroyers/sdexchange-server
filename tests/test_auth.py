from fastapi import status
from httpx import AsyncClient
from piccolo.apps.user.tables import BaseUser
import pytest

from app.main import app
from app.auth import crud


class TestAuth:
    @pytest.mark.asyncio
    async def test_login(self, client: AsyncClient) -> None:
        creds = {'username': 'test_user', 'password': 'abc123'}
        user = BaseUser(**creds)
        await user.save()

        response = await client.post(app.url_path_for('token'), data=creds)
        assert response.status_code == status.HTTP_200_OK
        assert 'access_token' in response.json()

    @pytest.mark.asyncio
    async def test_me(self, client: AsyncClient, basic_user: BaseUser) -> None:
        response = await client.get(app.url_path_for('me'))
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['username'] == basic_user.username

    @pytest.mark.asyncio
    async def test_me_not_logged_in(self, client: AsyncClient) -> None:
        response = await client.get(app.url_path_for('me'))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_update_user(self, client: AsyncClient, basic_user: BaseUser) -> None:
        update_data = {'first_name': 'Updateme', 'last_name': 'Plz'}
        response = await client.patch(app.url_path_for('update_user_me'), json=update_data)
        updated_user = await crud.get_user(basic_user.id)
        assert response.status_code == status.HTTP_200_OK
        assert updated_user.first_name == update_data['first_name']

    @pytest.mark.asyncio
    async def test_update_user_password(self, client: AsyncClient, basic_user: BaseUser) -> None:
        update_data = {'current_password': 'test123', 'password': 'newpassword'}
        response = await client.post(app.url_path_for('update_password_me'), json=update_data)
        print(response.content)
        assert response.status_code == status.HTTP_200_OK
        assert await BaseUser.login(basic_user.username, 'newpassword') == basic_user.id
