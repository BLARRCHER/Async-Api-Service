import json
from abc import ABC, abstractmethod
from typing import Any

import backoff
from redis import asyncio as aioredis
from redis.exceptions import RedisError

from core.config import redis_settings


class AsyncCacheService(ABC):
    @abstractmethod
    async def put_data(self, key: str, data: Any) -> Any | None:
        pass

    @abstractmethod
    async def get_data(self, key: str) -> list[Any] | None:
        pass


class RedisCacheService(AsyncCacheService):

    def __init__(self, redis_connector: aioredis.Redis):
        self.redis = redis_connector

    @backoff.on_exception(
        backoff.expo, RedisError, max_time=10)
    async def put_data(self, key: str, data: Any):
        if not data:
            return
        await self.redis.set(key, json.dumps(data), ex=redis_settings.TTL)

    @backoff.on_exception(
        backoff.expo, RedisError, max_time=10)
    async def get_data(self, key):
        data = await self.redis.get(key)
        if not data:
            return None
        return json.loads(data.decode("utf-8"))
