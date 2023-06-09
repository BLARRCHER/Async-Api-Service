"""Fixtures for persons service."""
import pytest
from tests.functional.settings import el_config
from tests.functional.utils.elastic_test_schemas import persons_index_schema
from tests.functional.utils.elastic_test_service import ElasticTestService


@pytest.fixture
async def prepare_person_service(es_client, load_test_persons_to_es):
    """Create test person_ index to es and delete after."""
    es_service = ElasticTestService(es_client)
    await es_service.create_index(
        el_config.INDEXES['person'], persons_index_schema)
    await es_service.bulk_store(
        el_config.INDEXES['person'], load_test_persons_to_es)
    yield


@pytest.fixture
def load_test_persons_to_es(load_test_data):
    return load_test_data('persons_load_to_es.json')


@pytest.fixture
def expected_persons_list(load_test_data):
    return load_test_data('persons_load_to_es.json')


@pytest.fixture
def expected_person_detail(load_test_data):
    return load_test_data('person_detail.json')


@pytest.fixture
def expected_film_by_person(load_test_data):
    return load_test_data('film_search.json')


@pytest.fixture
def person_id():
    return "2d6f6284-13ce-4d25-9453-c4335432c116"


@pytest.fixture
def api_persons_v1_url():
    return '/api/v1/persons/'


@pytest.fixture
def api_person_by_id_v1_url():
    return '/api/v1/persons/{person_id}'


@pytest.fixture
def api_search_film_by_person():
    return '/api/v1/persons/{person_id}/film/'


@pytest.fixture
def api_search_person_by_query():
    return '/api/v1/persons/search/'
