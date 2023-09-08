from datetime import datetime

from minio import Minio


def get_client():
    from .env import MINIO_HOST, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_SECURE

    return Minio(
        MINIO_HOST,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=MINIO_SECURE,
    )


def store_output_in_s3(file_path, kind):
    target_file_path = _s3_file_name(kind=kind)
    get_client().fput_object(
        bucket_name="artifacts", object_name=target_file_path, file_path=file_path
    )

    return target_file_path


def _s3_file_name(kind):
    date_str = datetime.now().strftime("%Y%m%d")
    base_file_name = "source-main"

    return f"/j-en-v/{kind}/{base_file_name}--{date_str}.xlsx"
