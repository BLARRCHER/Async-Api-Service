import asyncio

from redis import asyncio as aioredis

from settings import redis_config
from utils.backoff import backoff


class FailConnectinonRedis(Exception):
    pass


@backoff(start_sleep_time=1, factor=2, border_sleep_time=20)
async def wait_redis():
    try:
        re = aioredis.from_url(
            f"redis://{redis_config.HOST}:{redis_config.PORT}")
        await re.ping()
    except aioredis.exceptions.ConnectionError:
        raise FailConnectinonRedis('Fail connectinon to Redis')


if __name__ == '__main__':
    asyncio.run(wait_redis())
