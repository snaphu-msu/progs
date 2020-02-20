import numpy as np
import pandas as pd

# progs
from . import paths
from . import config


def load_prog(mass, series, verbose=True):
    """Load progenitor model from file

    parameters
    ----------
    mass : float/int
    series : str
    verbose : bool
    """
    conf = config.load_config(series, verbose)
    cols = config.get_column_list(conf)

    raw = load_raw(mass, series, verbose=verbose)

    return raw


def load_raw(mass, series, verbose=True):
    """Load raw progenitor model from file

    parameters
    ----------
    mass : float/int
    series : str
    verbose : bool
    """
    conf = config.load_config(series, verbose)
    filepath = paths.prog_filepath(mass, series)

    raw = pd.read_csv(filepath, delim_whitespace=conf['load']['delim_whitespace'],
                      skiprows=conf['load']['skiprows'], header=None)

    return raw
