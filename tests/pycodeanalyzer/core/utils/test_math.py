import pytest

from pycodeanalyzer.core.utils.math import round_up

class TestMath:

    def test_round_up(self):
        assert round_up(10.1, 0) == 11
        assert round_up(10.1, 1) == 10.1
        assert round_up(10.12, 1) == 10.2
        assert round_up(10.10, 1) == 10.1
        assert round_up(10.101, 3) == 10.101
        assert round_up(10.1011, 3) == 10.102
