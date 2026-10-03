from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "database.db"
    class Config:
        env_file: str = ".env"