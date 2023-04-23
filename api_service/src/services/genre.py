from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis import asyncio as aioredis

from db.elastic import get_elastic
from db.redis import get_redis
from services.base import BaseService
from services.cache_service import RedisCacheService
from services.search_service import ElasticSearchEngine


class GenreService(BaseService):
    index = 'genre'


@lru_cache()
def get_genre_service(
        redis: aioredis.Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> BaseService:
    return GenreService(
        search_engine=ElasticSearchEngine(elastic),
        cache_service=RedisCacheService(redis)
    )
