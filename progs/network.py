import numpy as np
import pandas as pd


"""
Handle nuclear network information
"""


def get_sums(composition, network):
    """Calculate summed quantities from isotope composition
    
    Returns : pd.DataFrame
    
    parameters
    ----------
    composition : pd.DataFrame
        profile of isotope mass fractions
    network : pd.DataFrame
        profile of isotopes to sum over, as returned by load_net().
        isotope labels must match the column names in `composition`
    """
    sums_dict = {}
    n_zones = len(composition)

    for key in ['sumx', 'sumy', 'ye']:
        sums_dict[key] = np.zeros(n_zones)

    for _, isotope in network.iterrows():
        x = np.array(composition[isotope['isotope']], dtype=float)

        sums_dict['sumx'] += x
        sums_dict['sumy'] += x / isotope['A']
        sums_dict['ye'] += x * (isotope['Z'] / isotope['A'])

    sums_dict['abar'] = 1 / sums_dict['sumy']
    sums = pd.DataFrame(sums_dict)

    return sums
