from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name : str = "cool api"
    app_env : str
    debug : bool = False

    database_url : str

    model_config = SettingsConfigDict(extra="ignore")

settings = Settings()