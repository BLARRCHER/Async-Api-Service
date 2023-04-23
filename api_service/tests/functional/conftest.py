import asyncio
import os
from dataclasses import dataclass

import aiohttp
from redis import asyncio as aioredis
import orjson
import pytest
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy
from tests.functional.settings import (BASE_DIR, el_config, redis_config,
                                       service_config)

pytest_plugins = (
    "tests.functional.utils.film_conftest",
    "tests.functional.utils.persons_conftest",
    "tests.functional.utils.genre_conftest",
)


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
async def redis_client():
    redis = aioredis.from_url(
        f"redis://{redis_config.HOST}:{redis_config.PORT}")
    yield redis
    await redis.close()
    await redis.connection_pool.disconnect()


@pytest.fixture()
async def clear_redis_cache(redis_client):
    yield redis_client
    await redis_client.flushall()


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=f'{el_config.HOST}:{el_config.PORT}')
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(api_url: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = f'http://{service_config.HOST}:{service_config.PORT}' + api_url
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
def load_test_data():
    def load_data(filename: str):
        with open(os.path.join(BASE_DIR, 'testdata', filename)) as file:
            return orjson.loads(file.read())
    return load_data
