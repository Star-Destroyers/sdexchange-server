from pydantic import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    APP_NAME: str = 'StarDestroyers'
    # LASAIR_STORED_QUERY: str = '2Roys_TDE-candidates'
    LASAIR_STORED_QUERY: str = 'lasair_2AllnucleartransientsandTDEcandidates'
    DATABASE_URL: PostgresDsn = 'postgres://postgres:postgres@localhost:5432/tdeexchange'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_KEY: str


settings = Settings()
