from db.es_db import ElasticBase
from elasticsearch import helpers
from elasticsearch import TransportError
from el_index import MOVIES_INDEX_BODY, PERSON_INDEX_BODY, GENRE_INDEX_BODY
from typing import Generator
from loguru import logger


index_map = {
    'movies': MOVIES_INDEX_BODY,
    'person': PERSON_INDEX_BODY,
    'genre': GENRE_INDEX_BODY
}


class ESLoader(ElasticBase):
    def create_index(self, index: str):
        try:
            self.client.indices.create(index, body=index_map[index])
        except TransportError as ex:
            logger.warning(ex)

    def generate_elastic_data(self, index_name: str, data: list) -> Generator:
        for item in data:
            yield {
                '_id': item.uuid,
                '_index': index_name,
                **item.dict(),
            }

    def save_bulk(self, index: str, data: list) -> None:
        if index in index_map:
            self.create_index(index)

        res, _ = helpers.bulk(
            self.client,
            self.generate_elastic_data(index, data)
        )
        logger.info(f'Синхронизированно записей {res}')
