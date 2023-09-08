from unittest.mock import patch

import time_machine


class TestS3FileName:
    @time_machine.travel("2021-02-01 00:00:00")
    def test_s3_file_name_orgs(self):
        from util.s3 import _s3_file_name

        file_name = _s3_file_name(kind="orgs")
        expected = "/j-en-v/orgs/source-main--20210201.xlsx"

        assert file_name == expected, "File name should be generated correctly"

    @time_machine.travel("2021-02-01 00:00:00")
    def test_s3_file_name_themes(self):
        from util.s3 import _s3_file_name

        file_name = _s3_file_name(kind="themes")
        expected = "/j-en-v/themes/source-main--20210201.xlsx"

        assert file_name == expected, "File name should be generated correctly"
