import numpy as np


def get_enclosed_mass(zone_mass):
    """Calculate enclosed mass by integrating zone mass

    Returns: np.array

    parameters
    ----------
    zone_mass : [flt]
    """
    zone_mass = np.array(zone_mass)
    enc_mass = [zone_mass[0]]

    for zm in zone_mass[1:]:
        enc_mass += [enc_mass[-1] + zm]

    enc_mass = np.array(enc_mass)

    return enc_mass
