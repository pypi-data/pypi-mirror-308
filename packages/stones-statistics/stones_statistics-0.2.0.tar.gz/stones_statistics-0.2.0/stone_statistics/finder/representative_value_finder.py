from fractions import Fraction
from .. import stat


def mean_finder(values: list[Fraction], coefficient: int, mean: Fraction) -> Fraction:
    s = sum(values)
    m2 = mean * (len(values) + coefficient)
    return (m2 - s) * Fraction(1, coefficient)


def median_finder(values: list[Fraction], coefficient: int, median: Fraction) -> Fraction | None:
    v2 = values[:]
    for i in range(coefficient):
        v2.append(median)
    if Stat.median(v2) != median:
        return None
    else:
        return median


@DeprecationWarning
def mode_finder(values: list[Fraction], mode: Fraction) -> Fraction | None:
    """It is useless"""
    return None
