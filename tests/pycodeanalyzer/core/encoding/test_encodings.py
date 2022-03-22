import pytest

from pycodeanalyzer.core.encoding.encodings import Encoding

class TestEncoding:

    def test_getFileEncoding(self, mocker):
        filepath = "titi/toto/tutu.txt"
        expected = "utf-8"
        encoding = Encoding()
        encoding.magic.from_file = mocker.MagicMock(return_value=expected)
        res = encoding.getFileEncoding(filepath)
        assert encoding.magic.from_file.call_count == 1
        assert res == expected
