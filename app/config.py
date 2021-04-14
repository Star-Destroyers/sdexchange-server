from pydantic import BaseSettings
from pydantic import PostgresDsn

class Settings(BaseSettings):
    APP_NAME: str = 'StarDestroyers'
    LASAIR_STORED_QUERY: str = '2Roys_TDE-candidates'
    DATABASE_URL: PostgresDsn = 'postgres://postgres:postgres@localhost:5432/tdeexchange'


settings = Settings()
