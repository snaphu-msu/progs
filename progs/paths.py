import os

aliases = {
    's16': 'sukhbold_2016',
    's18': 'sukhbold_2018',
}


# ===============================================================
#                      Repo/meta
# ===============================================================
def repo_path():
    """Return path to progs repo
    """
    try:
        path = os.environ['PROGS']
    except KeyError:
        raise EnvironmentError('Environment variable PROGS not set. '
                               'Set path to progs repo directory, e.g., '
                               "'export PROGS=${HOME}/codes/progs'")
    return path


def progs_path():
    """Return path to top-level directory of progenitors
    """
    try:
        path = os.environ['PROGENITORS']
    except KeyError:
        raise EnvironmentError('Environment variable PROGENITORS not set. '
                               'Set path to progenitors top-level directory, e.g., '
                               "'export PROGENITORS=${HOME}/data/progenitors'")
    return path


def config_filepath(series):
    """Return path to config file

    parameters
    ----------
    series : str
    """
    path = repo_path()
    series = check_alias(series)
    return os.path.join(path, 'progs', 'config', f'{series}.ini')


# ===============================================================
#                      Progs
# ===============================================================
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
    s_path = series_path(series)
    filename = prog_filename(mass, series=series)
    return os.path.join(s_path, filename)


def series_path(series):
    """Return path to progenitor series directory

    parameters
    ----------
    series : str
    """
    path = progs_path()
    series = check_alias(series)
    return os.path.join(path, series)


# ===============================================================
#                      Misc.
# ===============================================================
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
