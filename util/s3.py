from datetime import datetime

from minio import Minio


def get_client():
    from .env import MINIO_HOST, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_SECURE

    return Minio(
        MINIO_HOST,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=MINIO_SECURE
    )


def store_output_in_s3(file_path):
    get_client().fput_object(
        bucket_name='artifacts',
        object_name=_s3_file_name(),
        file_path=file_path
    )


def _s3_file_name():
    from .env import ENGINE_NAME, SUB_SOURCE_FILTER

    date_str = datetime.now().strftime('%Y%m%d')
    base_file_name = ENGINE_NAME
    if type(SUB_SOURCE_FILTER) is str and len(SUB_SOURCE_FILTER) > 0:
        base_file_name = f"{base_file_name}--{SUB_SOURCE_FILTER}"

    return f"/j-en-v-orgs/{base_file_name}--{date_str}.xlsx"
