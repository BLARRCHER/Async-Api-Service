"""Fixtures for genres service."""
import pytest
from tests.functional.settings import el_config
from tests.functional.utils.elastic_test_schemas import genres_index_schema
from tests.functional.utils.elastic_test_service import ElasticTestService


@pytest.fixture
async def prepare_genre_service(es_client, load_test_genres_to_es):
    """Create test person_ index to es and delete after."""
    es_service = ElasticTestService(es_client)
    await es_service.create_index(
        el_config.INDEXES['genre'], genres_index_schema)
    await es_service.bulk_store(
        el_config.INDEXES['genre'], load_test_genres_to_es)
    yield


@pytest.fixture
def load_test_genres_to_es(load_test_data):
    return load_test_data('genres_loads_to_es.json')


@pytest.fixture
def expected_genres_list(load_test_data):
    return load_test_data('genres_loads_to_es.json')


@pytest.fixture
def expected_genre_detail(load_test_data):
    return load_test_data('genre_by_id.json')


@pytest.fixture
def genre_id():
    return "e508c1c8-1111-4136-80b4-340c4befb190"


@pytest.fixture
def api_genre_v1_url():
    return '/api/v1/genres/'


@pytest.fixture
def api_genre_by_id_v1_url():
    return '/api/v1/genres/{genre_id}'
