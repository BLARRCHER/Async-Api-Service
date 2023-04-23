import os

from pydantic import BaseSettings, Field

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ServiceSettings(BaseSettings):
    """ Настройки подключения к API """
    HOST: str = '127.0.0.1'
    PORT: int = Field(default='8000')

    class Config:
        env_prefix = 'SERVICE_'


class ElasticSettings(BaseSettings):
    """ Настройки подключения к Elastic. """
    HOST: str = '127.0.0.1'
    PORT: int = Field(default='9200')
    INDEXES: dict[str, str] = {
        'movies': 'movies', 'person': 'person', 'genre': 'genre'
    }

    class Config:
        env_prefix = 'ELASTIC_'


class RedisSettings(BaseSettings):
    """ Настройки подключения к Redis. """
    HOST: str = '127.0.0.1'
    PORT: int = Field(default='6379')
    TTL: int = 60 * 5

    class Config:
        env_prefix = 'REDIS_'


service_config = ServiceSettings()
el_config = ElasticSettings()
redis_config = RedisSettings()
