"""Fixtures for filmworks service tests."""
import json
import uuid

import pytest
from tests.functional.settings import el_config
from tests.functional.utils.elastic_test_schemas import filmworks_index_schema
from tests.functional.utils.elastic_test_service import ElasticTestService


def get_es_bulk_query(data, index, id_field):
    bulk_query = []
    for row in data:
        bulk_query.extend([
            json.dumps({'index': {'_index': index,
                                  '_id': row[id_field]}}),
            json.dumps(row)
        ])
    return bulk_query


@pytest.fixture
async def prepare_film_service(es_client, load_test_films_to_es):
    """Create test index for tests and delete index after."""
    es_service = ElasticTestService(es_client)
    await es_service.create_index(
        el_config.INDEXES['movies'], filmworks_index_schema)
    yield es_service
    await es_service.delete_index('movies')


@pytest.fixture
def load_films_to_es(prepare_film_service):
    async def inner(load_test_films: dict):
        bulk_query = get_es_bulk_query(
            load_test_films, 'movies', 'uuid')
        str_query = '\n'.join(bulk_query) + '\n'
        response = await prepare_film_service.es.bulk(str_query, refresh=True)
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture
async def prepare_films_from_testdata(load_films_to_es, load_test_films_to_es):
    await load_films_to_es(load_test_films_to_es)


@pytest.fixture
def gen_film_data(expected_film_detail):
    def inner(range_int: int = 10):
        films = []
        for i in range(range_int):
            prepared_film_copy = expected_film_detail.copy()
            prepared_film_copy['uuid'] = str(uuid.uuid4())
            films.append(prepared_film_copy)
        return films
    return inner


@pytest.fixture
def load_test_films_to_es(load_test_data):
    return load_test_data('films_loads_to_es.json')


@pytest.fixture
def api_films_v1_base_url():
    return '/api/v1/films'


@pytest.fixture
def api_film_by_id_v1_url(api_films_v1_base_url):
    return api_films_v1_base_url + '/{film_id}'


@pytest.fixture
def api_film_by_query_v1_url(api_films_v1_base_url):
    return api_films_v1_base_url + '/search'


@pytest.fixture
def film_id():
    return "e4626af1-7fd5-414b-ba82-555555555555"


@pytest.fixture
def expected_films_list(load_test_data):
    return load_test_data('film_list.json')


@pytest.fixture
def expected_film_detail(load_test_data):
    return load_test_data('film_by_id.json')


@pytest.fixture
def expected_film_search(load_test_data):
    return load_test_data('film_search.json')
