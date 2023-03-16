from unittest.mock import patch

import time_machine


class TestS3FileName:
    @time_machine.travel('2021-02-01 00:00:00')
    @patch('util.env.ENGINE_NAME', 'test-engine')
    @patch('util.env.SOURCES', '')
    def test_s3_file_name(self):
        from util.s3 import _s3_file_name

        file_name = _s3_file_name()
        expected = '/j-en-v-orgs/test-engine--20210201.xlsx'

        assert file_name == expected, "File name should be generated correctly"

    @time_machine.travel('2021-02-01 00:00:00')
    @patch('util.env.ENGINE_NAME', 'test-engine')
    @patch('util.env.SOURCES', 'sample,test')
    def test_s3_file_name(self):
        from util.s3 import _s3_file_name

        file_name = _s3_file_name()
        expected = '/j-en-v-orgs/test-engine--sample_test--20210201.xlsx'

        assert file_name == expected, "File name should be generated correctly"
