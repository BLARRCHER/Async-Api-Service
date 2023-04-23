import logging

import uvicorn as uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination
from redis import asyncio as aioredis

from core.config import app_settings, elastic_settings, redis_settings
from core.logger import LOGGING
from db import elastic, redis
from routers.base import api

app = FastAPI(
    title=app_settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    # Подключаемся к базам при старте сервера
    # Подключиться можем при работающем event-loop
    # Поэтому логика подключения происходит в асинхронной функции
    redis.redis = aioredis.from_url(
        f"redis://{redis_settings.host}:{redis_settings.port}")
    elastic.es = AsyncElasticsearch(
        hosts=[f'{elastic_settings.host}:{elastic_settings.port}'])


@app.on_event('shutdown')
async def shutdown():
    # Отключаемся от баз при выключении сервера
    await redis.redis.close()
    await elastic.es.close()


app.include_router(api, prefix="/api")
add_pagination(app)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8080,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
