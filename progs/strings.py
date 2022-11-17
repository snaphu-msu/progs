"""
Module for formatting/printing strings
"""


def check_alias(series):
    """Return full name of series if alias used

    parameters
    ----------
    series : str
    """
    aliases = {
        's16': 'sukhbold_2016',
        's18': 'sukhbold_2018',
        'WH02': 'wh_02',
        'WH_02': "wh_02"
    }

    if series in aliases:
        return aliases[series]
    else:
        return series
