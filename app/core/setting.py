import os
import sys

from dotenv import load_dotenv

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    env_path = os.path.join(sys._MEIPASS, "env")
else:
    env_path = os.path.join(os.path.dirname(__file__), "..", "..")

env_path = os.path.join(env_path, ".env")
load_dotenv(env_path)


APP_ENV = os.environ.get("APP_ENV")
DEBUG = bool(os.environ.get("DEBUG"))
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS").split(",")

# from pydantic import field_validator
# from pydantic_settings import BaseSettings, SettingsConfigDict
#
#
# class EnvSettings(BaseSettings):
#     APP_ENV: str
#     DEBUG: bool
#     ALLOWED_ORIGINS: str
#
#     @field_validator("ALLOWED_ORIGINS")
#     def parsing_allowed_origins(cls, value):
#         if isinstance(value, str):
#             return [i.strip() for i in value.split(",")]
#         return value
#
#
# class GlobalSettings(BaseSettings):
#     ENV_STATE: str = "dev"
#
#     model_config = SettingsConfigDict(env_file="env/base.env")
#
#
# class DevSettings(EnvSettings):
#     model_config = SettingsConfigDict(env_file="env/dev.env")
#
#
# class ProdSettings(EnvSettings):
#     model_config = SettingsConfigDict(env_file="env/prod.env")
#
#
# class FactorySettings:
#     @staticmethod
#     def load():
#         env_state = GlobalSettings().ENV_STATE
#         if env_state == "dev":
#             return DevSettings()
#         elif env_state == "prod":
#             return ProdSettings()
#
#
# settings = FactorySettings.load()
