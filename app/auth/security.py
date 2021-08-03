from fastapi_users.authentication import JWTAuthentication
from app.config import settings


auth_backends = []

jwt_authentication = JWTAuthentication(secret=settings.SECRET_KEY, lifetime_seconds=3600, tokenUrl="auth/jwt/login")

auth_backends.append(jwt_authentication)
