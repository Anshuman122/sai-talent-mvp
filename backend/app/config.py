from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    APP_NAME: str = "SAI Talent Assessment"
    SECRET_KEY: str = "your_super_secret_key"
    
    
    DATABASE_URL: str = "sqlite:///./sai_talent.db"

    
    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()