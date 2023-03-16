from unittest.mock import patch


@patch.dict('os.environ', {
    'ENGINE_NAME': 'dummy-ENGINE_NAME',
    'SOURCES': 'dummy-SOURCES',
    'MINIO_HOST': 'dummy-MINIO_HOST',
    'MINIO_ACCESS_KEY': 'dummy-MINIO_ACCESS_KEY',
    'MINIO_SECRET_KEY': 'dummy-MINIO_SECRET_KEY',
    'MINIO_SECURE': '1',
}, clear=True)
def test_engine_name():
    from util.env import ENGINE_NAME, SOURCES, MINIO_HOST, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_SECURE

    assert ENGINE_NAME == 'dummy-ENGINE_NAME', "ENGINE_NAME env should be correct"
    assert SOURCES == 'dummy-SOURCES', "ENGINE_NAME env should be correct"
    assert MINIO_HOST == 'dummy-MINIO_HOST', "MINIO_HOST env should be correct"
    assert MINIO_ACCESS_KEY == 'dummy-MINIO_ACCESS_KEY', "MINIO_ACCESS_KEY env should be correct"
    assert MINIO_SECRET_KEY == 'dummy-MINIO_SECRET_KEY', "MINIO_SECRET_KEY env should be correct"
    assert MINIO_SECURE is True, "MINIO_SECURE env should be correct"
