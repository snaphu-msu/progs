import numpy as np
import pandas as pd

# progs
from . import paths
from . import configuration

# TODO:
#     - convert Lagrangian to Eulerian coordinates


def load_prog(mass, series, config=None, verbose=True):
    """Load progenitor model from file

    parameters
    ----------
    mass : float/int
    series : str
    config : dict
    verbose : bool
    """
    config = configuration.check_config(config, series=series, verbose=verbose)
    raw = load_raw(mass, series, config=config, verbose=verbose)
    prog = pd.DataFrame()

    for key, idx in config['columns'].items():
        prog[key] = raw[idx]

    return prog


def load_raw(mass, series, config=None, verbose=True):
    """Load raw progenitor model from file

    parameters
    ----------
    mass : float/int
    series : str
    config : dict
    verbose : bool
    """
    config = configuration.check_config(config, series=series, verbose=verbose)
    filepath = paths.prog_filepath(mass, series)

    delim_whitespace = config['load']['delim_whitespace']
    skiprows = config['load']['skiprows']

    raw = pd.read_csv(filepath, delim_whitespace=delim_whitespace, skiprows=skiprows,
                      header=None)
    return raw


