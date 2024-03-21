import os
from pydantic import field_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class GlobalSettings(BaseSettings):
    ENV_STATE: str = "dev"


class EnvSettings(BaseSettings):
    APP_ENV: str
    DEBUG: bool
    ALLOWED_ORIGINS: str

    @field_validator("ALLOWED_ORIGINS")
    def parsing_allowed_origins(cls, value: str):
        if isinstance(value, str):
            return [i.strip() for i in value.split(",")]
        return value


class DevSettings(EnvSettings):
    pass


class ProdSettings(EnvSettings):
    pass


class FactorySettings:
    @staticmethod
    def load():
        try:
            local_env_path = os.path.join(os.path.dirname(__file__), "..", "..", "env")
            load_dotenv(os.path.join(local_env_path, 'base.env'))
        except FileNotFoundError:
            raise Exception("Environment path not found.")

        global_settings = GlobalSettings()
        env_state = global_settings.ENV_STATE
        env_file_path = os.path.join(local_env_path, f"{env_state}.env")

        if env_state == "dev":
            return DevSettings(_env_file=env_file_path)
        else:
            return ProdSettings(_env_file=env_file_path)


settings = FactorySettings.load()
