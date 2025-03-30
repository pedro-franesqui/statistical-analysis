"""
summary_statistics.py

This module provides implementations for summary
statistics computations, such as arithmetic and
geometric means, weighted means, median, mode,
centrality measures and quantiles, and graphical
representations for box plots

----------------------------------------------------
                 Summary Statistics
----------------------------------------------------

In order to describe values
    Xip, i = 1, ..., n, p = 1, ..., P
we use summary statistics. In general, a summary
statistic is any statistic that summarizes information
coming from a given variable, sets of variables, unit,
or sets of units.

Different types of data allow for the construction and
use of different types of summary statistics. Different
summary statistics may incorporate differently the
information present in the data.
"""

from collections import Counter
from typing import Union

__all__ = [
    "mean",
    "weighted_mean",
    "geometric_mean",
    "discrete_geometric_mean",
    "median",
    "grouped_freq_median",
    "get_percentile",
    "mode",
    "get_iqr"
]
__version__ = "1.0.0"
__author__ = "github: pedro-franesqui"


def mean(data: list=None) -> Union[int, float]:
    """
    Computes arithmetic mean of data passed as a list

    :param data: List of numbers (int or float) for which
                 arithmetic mean will be computed
    :type data: list
    :return: Arithmetic mean of numbers in the list
    :rtype: Union[int, float]
    """
    if data is None:
        raise ValueError("data must be provided")
    return sum(data) / len(data) if len(data) != 0 else 0

def weighted_mean(data: list=None, weights: list=None) -> Union[int, float]:
    """
    Computes weighted arithmetic mean of data passed
    as a list

    :param data: List of numbers (int or float) for which
                 weighted arithmetic mean will be computed
    :param weights: List of weights corresponding to each datum
    :type data: list
    :type weights: list
    :return: Weighted arithmetic mean
    :rtype: Union[int, float]
    """
    if data is None or weights is None:
        raise ValueError("Both data and weights must be provided")
    if len(data) != len(weights):
        raise ValueError("data and weights must have the same length")
    if len(data) == 0 :
        raise ValueError("data and weights must not be empty")
    if (total_weight := sum(weights)) == 0:
        raise ValueError("Total weight cannot be zero")
    return sum([i * j for i, j in zip(data, weights)]) / total_weight

def geometric_mean(data: list) -> Union[int, float]:
    """
    Computes geometric mean of data passed as a list

    :param data: List of numbers (int or float) for which
                 geometric mean will be computed
    :type data: list
    :return: Geometric mean of numbers in the list
    :rtype: Union[int, float]
    """
    if not data:
        raise ValueError("data must be provided")
    return _mul(data) ** (1 / len(data))

def discrete_geometric_mean(data: list[tuple]) -> float:
    """
    Computes geometric mean of a discrete variable
    with absolute frequencies

    :param data: List of tuples, where each tuple contains
                 (value, absolute frequency)
    :type data: list[tuple]
    :return: Geometric mean of the dataset
    :rtype: float
    """
    if not data:
        raise ValueError("data must be provided")

    product: float = 1
    total_freq: int = 0
    for value, freq in data:
        if freq < 0:
            raise ValueError(f"Frequency must be non-negative but {freq} was given")
        product *= value ** freq
        total_freq += freq

    if total_freq == 0:
        raise ValueError("Total frequency cannot be zero")

    return product ** (1 / total_freq)

def median(data: list) -> Union[int, float]:
    """
    Computes median of a dataset

    :param data: List of values for which the median will
                 be determined
    :type data: list
    :return: Median of the dataset
    :rtype: Union[int, float]
    """
    if not data:
        raise ValueError("data must be provided")

    sorted_data = sorted(data)
    n = len(sorted_data)
    mid: int = n // 2

    if n % 2 == 1:
        return sorted_data[mid]
    else:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2

def grouped_freq_median(classes: list[tuple], frequencies: list) -> float:
    """
    Computes median of a grouped frequency distribution

    :param classes: List of tuples, where each tuple represents the lower
                    and upper bounds for the class
    :param frequencies: List of frequencies corresponding to each class
    :type classes: list[tuple]
    :type frequencies: list
    :return: Median value of the grouped frequency distribution
    :rtype: float
    """
    return get_percentile(classes, frequencies, 0.5)

def get_percentile(classes: list[tuple],
                   frequencies: list,
                   k: Union[int, float],
                   percentage: bool=False) -> float:
    """
    Computes the kth percentile of a grouped frequency distribution

    :param classes: List of tuples, where each tuple represents the lower
                    and upper bounds for the class
    :param frequencies: List of frequencies corresponding to each class
    :param k: Percentile to be calculated
    :param percentage: Flag to indicate whether k is being passed as a decimal
                       with value between 0 and 1 or as a percentage
    :type classes: list[tuple]
    :type frequencies: list
    :type k: Union[int, float]
    :type percentage: bool
    :return: Value of the kth percentile
    :rtype: float
    """
    if not classes:
        raise ValueError("data must be provided")
    if not frequencies:
        raise ValueError("frequencies must be provided")

    if percentage:
        k /= 100
    n: int = sum(frequencies)
    pos: float = k * n

    cumulative_freq = 0
    for i, ((lower, upper), freq) in enumerate(zip(classes, frequencies)):
        prev_cumulative_freq = cumulative_freq
        cumulative_freq += freq
        if cumulative_freq >= pos:
            rel_prev_cumulative_freq = prev_cumulative_freq / n
            rel_cumulative_freq = cumulative_freq / n
            class_width = upper - lower
            numerator = k - rel_prev_cumulative_freq
            denominator = rel_cumulative_freq - rel_prev_cumulative_freq
            return (numerator/denominator) * class_width + lower
    else:
        raise ValueError("Unable to determine percentile class")

def mode(data: list) -> Union[int, float, list]:
    """
    Computes the mode (unimodal or multimodal) of a dataset

    :param data: List of values for which the mode will be determined
    :type data: list
    :return: The mode if there is a single one, or a list of modes if
             there are multiple.
    :rtype: Union[int, float, list]
    """
    if not data:
        raise ValueError("data must be provided")

    count_freq: Counter = Counter(data)
    max_freq: int = max(count_freq.values())
    modes = [value for value, freq in count_freq.items() if freq == max_freq]

    return modes[0] if len(modes) == 1 else sorted(modes)

def get_iqr(classes: list[tuple], frequencies: list) -> Union[int, float]:
    """
    Computes IQR (Inter-Quartile Range) of a grouped frequency distribution

    :param classes: List of tuples, where each tuple represents the lower
                    and upper bounds for the class
    :param frequencies: List of frequencies corresponding to each class
                        Percentile to be calculated
    :type classes: list[tuple]
    :type frequencies: list
    :return: IQR value
    :rtype: Union[int, float]
    """
    q1 = get_percentile(classes, frequencies, 0.25)
    q3 = get_percentile(classes, frequencies, 0.75)
    return q3 -q1

def get_max(classes: list[tuple[int]]) -> int:
    n_max: int  = max(classes)
    if n_max[0] < n_max[1]:
        return n_max[1]
    else:
        raise ValueError(f"Tuple {n_max} should contain (lower, upper)")

def get_min(classes: list[tuple]) -> int:
    n_min: int = min(classes)
    if n_min[0] < n_min[1]:
        return n_min[0]
    else:
        raise ValueError(f"Tuple {n_min} should contain (lower, upper)")


# Private #

def _mul(lst: list) -> Union[int, float]:
    """
    Computes product of a sequence passed as a list

    :param lst: list of numbers for which product will be
        computed
    :type lst: list
    :return: product of the numbers in the list
    :rtype: float
    """
    if lst is None:
        raise ValueError("List must be provided")
    if len(lst) == 0:
        return 0.0
    res: int = 1
    for i in lst:
        res *= i
        if i == 0: break
    return res