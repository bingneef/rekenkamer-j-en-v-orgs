from unittest.mock import patch


@patch.dict('os.environ', {
    'ENGINE_NAME': 'dummy-ENGINE_NAME',
    'SUB_SOURCE_FILTER': 'dummy-SUB_SOURCE_FILTER',
    'MINIO_HOST': 'dummy-MINIO_HOST',
    'MINIO_ACCESS_KEY': 'dummy-MINIO_ACCESS_KEY',
    'MINIO_SECRET_KEY': 'dummy-MINIO_SECRET_KEY',
    'MINIO_SECURE': '1',
}, clear=True)
def test_engine_name():
    from util.env import ENGINE_NAME, SUB_SOURCE_FILTER, MINIO_HOST, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_SECURE

    assert ENGINE_NAME == 'dummy-ENGINE_NAME', "ENGINE_NAME env should be correct"
    assert SUB_SOURCE_FILTER == 'dummy-SUB_SOURCE_FILTER', "SUB_SOURCE_FILTER env should be correct"
    assert MINIO_HOST == 'dummy-MINIO_HOST', "MINIO_HOST env should be correct"
    assert MINIO_ACCESS_KEY == 'dummy-MINIO_ACCESS_KEY', "MINIO_ACCESS_KEY env should be correct"
    assert MINIO_SECRET_KEY == 'dummy-MINIO_SECRET_KEY', "MINIO_SECRET_KEY env should be correct"
    assert MINIO_SECURE is True, "MINIO_SECURE env should be correct"
