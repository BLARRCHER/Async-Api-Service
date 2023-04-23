import os
from os.path import join
from db.pg_db import PostgresBase
from datetime import datetime
from loguru import logger


class PGExtractor(PostgresBase):

    def _get_sql_query(self, index_name: str):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path_sql_query = join(dir_path, f'sql_query/{index_name}.sql')
        with open(path_sql_query) as f:
            return f.read()

    def pg_loader(self, index_name: str, curren_state):
        curren_state = curren_state if curren_state else datetime.min
        sql_query = self._get_sql_query(index_name)
        self.cursor.execute(sql_query % curren_state)
        while True:
            records = self.cursor.fetchmany(self.batch)
            if not records:
                break
            yield records
