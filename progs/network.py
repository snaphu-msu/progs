import numpy as np
import pandas as pd

# progs
from . import paths

"""
Functions for handling nuclear network information
"""


def load_network(network_name):
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
    sums = {}
    n_zones = len(composition)

    for key in ['sumx', 'sumy', 'ye']:
        sums[key] = np.zeros(n_zones)

    for _, isotope in network.iterrows():
        x = np.array(composition[isotope['isotope']], dtype=float)

        sums['sumx'] += x
        sums['sumy'] += x / isotope['A']
        sums['ye'] += x * (isotope['Z'] / isotope['A'])

    sums['abar'] = 1 / sums['sumy']
    table = pd.DataFrame(sums)

    return table
