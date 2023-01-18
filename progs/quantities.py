import numpy as np
from astropy import units
from astropy import constants as const

cm_to_1k_km = units.cm.to(1e3 * units.km)
g_to_msun = units.g.to(units.M_sun)
sb = const.sigma_sb.cgs.value


def get_enclosed_mass(zone_mass):
    """Calculate enclosed mass by integrating zone mass

    Returns: np.array

    parameters
    ----------
    zone_mass : []
    """
    zone_mass = np.array(zone_mass)
    enc_mass = [zone_mass[0]]

    for zm in zone_mass[1:]:
        enc_mass += [enc_mass[-1] + zm]

    enc_mass = np.array(enc_mass)

    return enc_mass


def get_compactness(mass, radius):
    """Calculate compactness parameter

    Returns: np.array

    parameters
    ----------
    mass : []
        Enclosed mass (Msun)
    radius : []
        radius coordinate (cm)
    """
    mass = np.array(mass)
    radius = np.array(radius)

    compactness = mass / (radius * cm_to_1k_km)

    return compactness


def get_luminosity(radius, temperature):
    """Calculate blackbody luminosity

    Returns: np.array

    parameters
    ----------
    radius : []
        radius coordinate (cm)
    temperature : []
        Temperature coordinate (K)
    """
    radius = np.array(radius)
    temp = np.array(temperature)

    lum = 4 * np.pi * sb * radius**2 * temp**4

    return lum
