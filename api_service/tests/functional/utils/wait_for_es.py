from elasticsearch import Elasticsearch

from settings import el_config
from utils.backoff import backoff


class FailConnectinonElasticSearch(Exception):
    pass


@backoff(start_sleep_time=1, factor=2, border_sleep_time=10)
def wait_es():
    es = Elasticsearch(
        hosts=[el_config.HOST],
        port=el_config.PORT,
        verify_certs=True)
    if not es.ping():
        raise FailConnectinonElasticSearch('Fail connectinon to ElasticSearch')


if __name__ == '__main__':
    wait_es()
