"""
Module for formatting/printing strings
"""


def printv(string, verbose, **kwargs):
    """Print string if verbose is True

    parameters
    ----------
    string : str
    verbose : bool
    """
    if verbose:
        print(string, **kwargs)


def check_alias(series):
    """Return full name of series if alias used

    parameters
    ----------
    series : str
    """
    aliases = {
        's16': 'sukhbold_2016',
        's18': 'sukhbold_2018',
    }

    if series in aliases:
        return aliases[series]
    else:
        return series
