import os


# ===============================================================
#                      Repo/meta
# ===============================================================
def top_path():
    """Return path to top-level repo directory
    """
    path = os.path.join(os.path.dirname(__file__), '..')
    return path


def config_filepath(series):
    """Return path to config file

    parameters
    ----------
    series : str
    """
    filepath = os.path.join(top_path(), 'progs', 'config', f'{series}.ini')

    return filepath


def network_filepath(network):
    """Return path to table of given network

    parameters
    ----------
    network : str
    """
    filename = f'{network}.txt'
    filepath = os.path.join(top_path(), 'progs', 'networks', filename)

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
    filenames = {
        'sukhbold_2016': f's{mass}_presn',
        'wh_02': f's{mass}_presn',
    }

    filename = filenames.get(series)

    if filename is None:
        raise ValueError('Progenitor series not defined')

    return filename


def prog_filepath(mass, series):
    """Return filepath to progenitor model

    parameters
    ----------
    mass : float/int
    series : str
    """
    filename = prog_filename(mass, series=series)
    filepath = os.path.join(series_path(series), filename)

    return filepath


def series_path(series):
    """Return path to progenitor series directory

    parameters
    ----------
    series : str
    """
    series_dir = os.path.join(top_path(), 'progenitor_sets', series)

    return series_dir
