import os
from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ElasticSettings(BaseSettings):
    """ Настройки подключения к Elastic. """
    host: str = '127.0.0.1'
    port: int = Field(default="9200")

    class Config:
        env_prefix = 'ELASTIC_'


class RedisSettings(BaseSettings):
    """ Настройки подключения к Redis. """
    host: str = '127.0.0.1'
    port: int = Field(default="6379")
    TTL: int = 60 * 5

    class Config:
        env_prefix = 'REDIS_'


class AppSettings(BaseSettings):
    """ Настройки приложения. """
    project_name: str = 'movies'


redis_settings = RedisSettings()
elastic_settings = ElasticSettings()
app_settings = AppSettings()
