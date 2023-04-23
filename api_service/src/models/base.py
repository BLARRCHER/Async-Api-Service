from typing import Optional

import orjson
from pydantic import BaseModel, Field


class Filter(BaseModel):
    field: Optional[str]
    value: Optional[str]


class Page(BaseModel):
    number: int = Field(default=1, ge=1)
    size: int = Field(default=50, ge=1)


class QueryBase(BaseModel):
    query: Optional[str]
    sort: Optional[str]
    filter: Optional[Filter]
    page: Optional[Page] = Page()
    total: Optional[str] = 10000
    url: str = ''


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class ORJSONModel(BaseModel):

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
