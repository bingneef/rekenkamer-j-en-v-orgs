from unittest.mock import patch


@patch.dict(
    "os.environ",
    {
        "MINIO_HOST": "dummy-MINIO_HOST",
        "MINIO_ACCESS_KEY": "dummy-MINIO_ACCESS_KEY",
        "MINIO_SECRET_KEY": "dummy-MINIO_SECRET_KEY",
        "MINIO_SECURE": "1",
        "MONGO_CONNECTION_STRING": "dummy-MONGO_CONNECTION_STRING",
    },
    clear=True,
)
def test_engine_name():
    from util.env import (
        MINIO_HOST,
        MINIO_ACCESS_KEY,
        MINIO_SECRET_KEY,
        MINIO_SECURE,
        MONGO_CONNECTION_STRING,
    )

    assert MINIO_HOST == "dummy-MINIO_HOST", "MINIO_HOST env should be correct"
    assert (
        MINIO_ACCESS_KEY == "dummy-MINIO_ACCESS_KEY"
    ), "MINIO_ACCESS_KEY env should be correct"
    assert (
        MINIO_SECRET_KEY == "dummy-MINIO_SECRET_KEY"
    ), "MINIO_SECRET_KEY env should be correct"
    assert MINIO_SECURE is True, "MINIO_SECURE env should be correct"
    assert (
        MONGO_CONNECTION_STRING == "dummy-MONGO_CONNECTION_STRING"
    ), "MONGO_CONNECTION_STRING env should be correct"
