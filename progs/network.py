import pandas as pd
import os

# progs
from . import paths

"""
Functions for handling nuclear network information
"""


def load_net(network):
    """Load network table from file

    parameters
    ----------
    network : str
        name of network, e.g. 'net19'
    """
    filepath = paths.network_filepath(network)
    return pd.read_csv(filepath, delim_whitespace=True)
