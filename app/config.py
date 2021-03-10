from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME = 'StarDestroyers'


settings = Settings()
