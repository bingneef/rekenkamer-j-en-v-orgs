import os
import dotenv

dotenv.load_dotenv()

ENGINE_NAME = os.environ['ENGINE_NAME']
SUB_SOURCE_FILTER = os.environ["SUB_SOURCE_FILTER"]

MINIO_HOST = os.environ['MINIO_HOST']
MINIO_ACCESS_KEY = os.environ['MINIO_ACCESS_KEY']
MINIO_SECRET_KEY = os.environ['MINIO_SECRET_KEY']
MINIO_SECURE = os.environ['MINIO_SECURE'] == '1'
