from abc import ABC, abstractmethod
from typing import Any

import backoff
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import ConnectionError, NotFoundError

from models.base import QueryBase
from utils.query_maker import ElasticQueryMaker


class AsyncSearchEngine(ABC):
    @abstractmethod
    async def get_by_id(self, index: str, _id: str) -> Any | None:
        pass

    @abstractmethod
    async def get_by_ids(
            self, index: str, ids: list[str]) -> list[Any] | None:
        pass

    @abstractmethod
    async def get_by_query(
            self, index: str, params: QueryBase) -> list[Any] | None:
        pass


class ElasticSearchEngine(AsyncSearchEngine):

    def __init__(self, es_connector: AsyncElasticsearch):
        self.elastic = es_connector

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10)
    async def get_by_id(self, index: str, _id: str):
        try:
            doc = await self.elastic.get(index, _id)
            return doc['_source']
        except NotFoundError:
            return None

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10)
    async def get_by_query(self, index: str, params: QueryBase):
        body = ElasticQueryMaker(params).make_body()
        try:
            result = await self.elastic.search(index=index, body=body)
            data = [
                doc['_source']
                for doc in result['hits']['hits']
            ]
            return data
        except NotFoundError:
            return None

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10)
    async def get_by_ids(self, index: str, ids: list[str]) -> list[Any] | None:
        pass
