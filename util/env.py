import os

import dotenv

dotenv.load_dotenv()

MINIO_HOST = os.environ["MINIO_HOST"]
MINIO_ACCESS_KEY = os.environ["MINIO_ACCESS_KEY"]
MINIO_SECRET_KEY = os.environ["MINIO_SECRET_KEY"]
MINIO_SECURE = os.environ["MINIO_SECURE"] == "1"

MONGO_CONNECTION_STRING = os.environ["MONGO_CONNECTION_STRING"]
