"""Utility for containers type in Python.
"""

from typing import Any, List


def rindex(lst: List[Any], value: Any) -> Any:
    lst.reverse()
    i = lst.index(value)
    lst.reverse()
    return len(lst) - i - 1
