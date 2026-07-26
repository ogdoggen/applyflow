from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name : str = "cool api"
    app_env : str
    debug : bool = False

    model_config = SettingsConfigDict(env_file="../.env")