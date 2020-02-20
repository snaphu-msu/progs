import os

path = '~/projects/data/progenitors'

aliases = {
    's16': 'sukhbold_2016',
    's18': 'sukhbold_2018',
}


def prog_filename(mass, series):
    """Return filename of progenitor

    parameters
    ----------
    mass : float/int
    series : str
    """
    def s16(mass):
        return f's{mass}_presn'

    filenames = {
        'sukhbold_2016': s16,
    }

    series = check_alias(series)

    if series in filenames:
        return filenames[series](mass)
    else:
        raise ValueError('Progenitor series not defined')



def prog_filepath(mass, series):
    """Return filepath to progenitor model

    parameters
    ----------
    mass : float/int
    series : str
    """
    filename = prog_filename(mass, series=series)
    # filepath = os.path.join(


def series_path(series):
    """Return path to progenitor series directory

    parameters
    ----------
    series : str
    """
    series = check_alias(series)
    return os.path.join(path, series)


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
