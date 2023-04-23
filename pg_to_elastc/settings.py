import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

pg_dsl = {
    'dbname': os.environ.get('POSTGRES_DB'),
    'user': os.environ.get('POSTGRES_USER'),
    'password': os.environ.get('POSTGRES_PASSWORD'),
    'host': os.environ.get('POSTGRES_HOST', '127.0.0.1'),
    'port': os.environ.get('POSTGRES_PORT', 5432),
    'options': '-c search_path=public,content',
}

es_dsl = {
    'hosts': [os.environ.get('ELASTIC_HOST')],
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LocalStorage = join(dirname(__file__), 'storage.json')