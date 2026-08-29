from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name : str = "cool api"
    app_env : str
    debug : bool = False

    database_url : str
    test_database_url : str

    model_config = SettingsConfigDict(extra="ignore")

    secret_key : str
    jwt_algorithm : str
    access_token_expire_minutes : int

settings = Settings()