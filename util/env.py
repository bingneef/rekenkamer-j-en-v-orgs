import os

import dotenv

dotenv.load_dotenv()

ENGINE_NAME = os.environ['ENGINE_NAME']
SOURCES = os.environ['SOURCES']

MINIO_HOST = os.environ['MINIO_HOST']
MINIO_ACCESS_KEY = os.environ['MINIO_ACCESS_KEY']
MINIO_SECRET_KEY = os.environ['MINIO_SECRET_KEY']
MINIO_SECURE = os.environ['MINIO_SECURE'] == '1'

ELASTIC_ENTERPRISE_URL = os.environ['ELASTIC_ENTERPRISE_URL']
ELASTIC_APP_SEARCH_KEY = os.environ['ELASTIC_APP_SEARCH_KEY']
