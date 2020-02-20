import os

path = '~/projects/data/progenitors'

aliases = {
    's16': 'sukhbold_2016',
    's18': 'sukhbold_2018',
}


def get_prog_filename(mass, series):
    """Return filename of progenitor

    parameters
    ----------
    mass : float/int
    series : str
    """
    pass


def check_alias(series):
    """Return full name of series if alias used

    parameters
    ----------
    series : str
    """
    if series in aliases:
        return aliases[series]
    else:
        return series
