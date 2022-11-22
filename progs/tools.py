import numpy as np

"""
Misc. helper functions for general use
"""


def ensure_sequence(x):
    """Ensure given object is in the form of a sequence.
    If object is scalar, return as length-1 list.

    Returns : []

    parameters
    ----------
    x : 1D-array or scalar
    """
    if isinstance(x, (list, tuple, np.ndarray)):
        return x
    else:
        return [x, ]


def find_nearest_idx(array, value):
    """Return idx for the array element nearest to the given value

    Note: array assumed to be monotonically increasing (not enforced),
          will use the first element that exceeds the given value

    Returns : int

    parameters
    ----------
    array : 1D array
        array to search
    value : float
        value to look for in array
    """
    idx = np.searchsorted(array, value)
    if np.abs(value - array[idx - 1]) < np.abs(value - array[idx]):
        return idx - 1
    else:
        return idx
