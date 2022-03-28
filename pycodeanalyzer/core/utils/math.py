"""Math utility functions.
"""

import math


def round_up(n: float, decimals: int = 0) -> float:
    multiplier = 10**decimals
    return float(math.ceil(n * multiplier) / multiplier)
