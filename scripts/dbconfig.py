from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "./default.db"
    class Config:
        env_file: str = ".env"