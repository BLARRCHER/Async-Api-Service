from abc import ABC, abstractmethod

from models.base import QueryBase


class BaseQueryMaker(ABC):

    def __init__(self, params: QueryBase):
        self.params = params

    @abstractmethod
    def make_body(self) -> dict:
        return {}


class ElasticQueryMaker(BaseQueryMaker):

    def get_nested_filter(self, query: QueryBase):
        nested = dict()
        field = query.filter.field
        value = query.filter.value
        nested["nested"] = {
            "path": field,
            "query": {
                "bool": {"must": [
                    {"match": {field + ".name": value}},
                ]}
            }
        }
        return nested

    def get_search_query(self, query: QueryBase) -> dict:
        return {"multi_match": {"query": query.query}}

    def get_sort(self, query: QueryBase) -> dict:
        field = query.sort
        direction = 'asc'
        if field.startswith('-'):
            direction = 'desc'
            field = field[1:]
        return {field: {'order': direction}}

    def make_body(self) -> dict:
        body = dict()
        if self.params.query:
            body.setdefault('query', {}).update(
                self.get_search_query(self.params))
        if self.params.filter:
            body.setdefault('query', {}).update(
                self.get_nested_filter(self.params))
        if self.params.sort:
            body['sort'] = self.get_sort(self.params)
        if self.params.page:
            body['from'] = (
                (self.params.page.number - 1) * self.params.page.size
            )
            body['size'] = self.params.page.size
        return body
