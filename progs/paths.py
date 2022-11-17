import os


# ===============================================================
#                      Repo/meta
# ===============================================================
def repo_path():
    """Return path to progs repo
    """
    path = os.path.dirname(__file__)
    top_path = os.path.join(path, '..')

    return top_path


def progs_path():
    """Return path to top-level directory of progenitors
    """
    path = os.path.join(repo_path(), 'progenitor_sets')
    return path


def config_filepath(series):
    """Return path to config file

    parameters
    ----------
    series : str
    """
    path = repo_path()
    series = check_alias(series)
    filepath = os.path.join(path, 'progs', 'config', f'{series}.ini')

    return filepath


def network_filepath(network):
    """Return path to table of given network

    parameters
    ----------
    network : str
    """
    path = repo_path()
    filename = f'{network}.txt'
    filepath = os.path.join(path, 'progs', 'networks', filename)

    return filepath


# ===============================================================
#                      Progenitors
# ===============================================================
def prog_filename(mass, series):
    """Return filename of progenitor

    parameters
    ----------
    mass : float/int
    series : str
    """
    def s16(mass_):
        return f's{mass_}_presn'

    def wh02(mass_):
        return f"s{mass_}_presn"

    filenames = {
        'sukhbold_2016': s16,
        "wh_02": wh02,
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
    filepath = os.path.join(s_path, filename)

    return filepath


def series_path(series):
    """Return path to progenitor series directory

    parameters
    ----------
    series : str
    """
    path = progs_path()
    series = check_alias(series)
    series_dir = os.path.join(path, series)

    return series_dir


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
