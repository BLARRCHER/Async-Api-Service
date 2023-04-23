import time
from settings import es_dsl, pg_dsl, LocalStorage
from state import JsonFileStorage, State
from datetime import datetime, timezone
from models import FullPerson, Genre, Movies
from extractor import PGExtractor
from loader import ESLoader
from loguru import logger


def curren_date_iso():
    return datetime.now(timezone.utc).isoformat()


def extract(pg_db, index_name: str, curren_state):
    return pg_db.pg_loader(index_name, curren_state)


def transform(index_name: str, data):
    models = {
        'genre': Genre,
        'person': FullPerson,
        'movies': Movies
    }
    model = models.get(index_name)
    for batch in data:
        yield [model(**row) for row in batch]


def loader(es_db, index_name: str, data):
    for batch in data:
        es_db.save_bulk(index_name, batch)


def run(index_name: str, state: State):
    curren_state = state.get_state(index_name)
    with PGExtractor(pg_dsl) as pg_db, ESLoader(es_dsl) as es_db:
        logger.info(f'Соеденения установленны синхронизируем {index_name}')
        data = extract(pg_db, index_name, curren_state)
        data = transform(index_name, data)
        loader(es_db, index_name, data)
        now = curren_date_iso()
        state.set_state(index_name, now)


def main():
    storage = JsonFileStorage(LocalStorage)
    state = State(storage)
    indexes = ['movies', 'person', 'genre']
    for index_name in indexes:
        run(index_name, state)


if __name__ == '__main__':
    while True:
        main()
        time.sleep(10)
