import pytest

from pycodeanalyzer.core.utils.containers import rindex

class TestContainers:

    def test_rindex(self):
        assert rindex([1, 2 ,3 ,4 ,5 ,6], 6) == 5
        assert rindex([1, 2 ,3 ,4 ,5 ,6], 1) == 0
        assert rindex([1, 2 ,3 ,4 ,5 ,6], 4) == 3
        assert rindex([1, 2 ,3 ,4 ,5 ,1], 1) == 5
        assert rindex([1, 2 ,3 ,1 ,5 ,6], 1) == 3
