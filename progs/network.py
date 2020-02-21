import numpy as np
import pandas as pd

# progs
from . import paths

"""
Functions for handling nuclear network information
"""


def load_net(network_name):
    """Load network table from file

    parameters
    ----------
    network_name : str
        name of network, e.g. 'net19'
    """
    filepath = paths.network_filepath(network_name)
    return pd.read_csv(filepath, delim_whitespace=True)


def get_sums(composition, network):
    """Calculate summed quantities from isotope composition

    parameters
    ----------
    composition : pd.DataFrame
        table of isotope mass fractions
    network : pd.DataFrame
        table of isotopes to sum over, as returned by load_net().
        isotope labels must match the column names in `composition`
    """
    out = {}
    n_zones = len(composition)

    for key in ['sumx', 'sumy', 'ye']:
        out[key] = np.zeros(n_zones)

    for row in network.itertuples():
        x_i = np.array(composition[row.isotope])

        out['sumx'] += x_i
        out['sumy'] += x_i / row.A
        out['ye'] += x_i * (row.Z / row.A)

    return out
