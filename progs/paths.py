import os


# ===============================================================
#                      Repo/meta
# ===============================================================
def top_path():
    """Return path to top-level repo directory

    Returns : str
    """
    path = os.path.join(os.path.dirname(__file__), '..')
    return path


def config_filepath(progset_name):
    """Return path to config file

    Returns : str

    parameters
    ----------
    progset_name : str
    """
    filepath = os.path.join(top_path(), 'progs', 'config', f'{progset_name}.ini')

    return filepath


def network_filepath(network):
    """Return path to profile of given network

    Returns : str

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
def prog_filename(zams, progset_name):
    """Return filename of progenitor

    Returns : str

    parameters
    ----------
    zams : str
    progset_name : str
    """
    filenames = {
        'sukhbold_2016': f's{zams}_presn',
    }

    filename = filenames.get(progset_name)

    if filename is None:
        raise ValueError(f"Progenitor set '{progset_name}' not defined")

    return filename


def prog_filepath(zams, progset_name):
    """Return filepath to progenitor model

    Returns : str

    parameters
    ----------
    zams : str
    progset_name : str
    """
    filename = prog_filename(zams, progset_name=progset_name)
    filepath = os.path.join(progset_path(progset_name), filename)

    return filepath


def progset_path(progset_name):
    """Return path to progenitor set directory

    Returns : str

    parameters
    ----------
    progset_name : str
    """
    path = os.path.join(top_path(), 'progenitor_sets', progset_name)
    return path
