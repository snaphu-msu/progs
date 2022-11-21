import os


# ===============================================================
#                      Repo/meta
# ===============================================================
def top_path():
    """Return path to top-level repo directory
    """
    path = os.path.join(os.path.dirname(__file__), '..')
    return path


def config_filepath(set_name):
    """Return path to config file

    parameters
    ----------
    set_name : str
    """
    filepath = os.path.join(top_path(), 'progs', 'config', f'{set_name}.ini')

    return filepath


def network_filepath(network):
    """Return path to profile of given network

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
def prog_filename(mass, set_name):
    """Return filename of progenitor

    parameters
    ----------
    mass : str
    set_name : str
    """
    filenames = {
        'sukhbold_2016': f's{mass}_presn',
        'wh_02': f's{mass}_presn',
    }

    filename = filenames.get(set_name)

    if filename is None:
        raise ValueError(f"Progenitor set '{set_name}' not defined")

    return filename


def prog_filepath(mass, set_name):
    """Return filepath to progenitor model

    parameters
    ----------
    mass : str
    set_name : str
    """
    filename = prog_filename(mass, set_name=set_name)
    filepath = os.path.join(set_path(set_name), filename)

    return filepath


def set_path(set_name):
    """Return path to progenitor set directory

    parameters
    ----------
    set_name : str
    """
    path = os.path.join(top_path(), 'progenitor_sets', set_name)
    return path
