import asyncio

from utils.wait_for_es import wait_es
from utils.wait_for_redis import wait_redis

if __name__ == '__main__':
    asyncio.run(wait_redis())
    wait_es()
