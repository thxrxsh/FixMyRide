from pydantic_settings import BaseSettings
from decouple import config


class Settings(BaseSettings):
    database_hostname: str = config("DATABASE_HOSTNAME")
    database_port: str = config("DATABASE_PORT") 
    database_password: str = config("DATABASE_PASSWORD")
    database_name: str = config("DATABASE_NAME")
    database_username: str = config("DATABASE_USERNAME")
    secret_key: str = config("SECRET_KEY")
    algorithm: str = config("ALGORITHM")
    access_token_expire_minutes: float = config("ACCESS_TOKEN_EXPIRE_MINUTES")
    api_key: str = config("GOOGLE_DIRECTIONS_API_KEY")

Settings = Settings()
