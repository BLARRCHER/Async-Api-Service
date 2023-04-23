from models.base import QueryBase
from services.cache_service import AsyncCacheService
from services.search_service import AsyncSearchEngine


class BaseService:
    index = ''

    def __init__(
        self,
        search_engine: AsyncSearchEngine,
        cache_service: AsyncCacheService
    ):
        self.search_engine = search_engine
        self.cache_service = cache_service

        if self.index == '':
            raise NotImplementedError

    async def get_by_query(self, params: QueryBase = QueryBase()):
        data = await self.cache_service.get_data(params.url)
        if not data:
            data = await self.search_engine.get_by_query(
                index=self.index, params=params)
            if not data:
                return None
            await self.cache_service.put_data(params.url, data)
        return data

    async def get_by_id(self, _id: str):
        data = await self.cache_service.get_data(_id)
        if not data:
            data = await self.search_engine.get_by_id(
                index=self.index, _id=_id)
            if not data:
                return None
            await self.cache_service.put_data(_id, data)
        return data
