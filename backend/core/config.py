from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # PostgreSQL settings 
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # FastApi settings
    FASTAPI_PORT: int

    # JWT settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    EE_SECRET_KEY: str

    # Admin credentials 
    ADMIN_FIO: str
    ADMIN_EMAIL: EmailStr
    ADMIN_PASSWORD: str

    @property
    def POSTGRES_URL(self):
        return(f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
               f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}')
        
    @property
    def POSTGRES_CLEAR_URL(self):
        return(f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
               f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}')
        
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
settings = Settings()