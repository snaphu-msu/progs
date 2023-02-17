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


def get_centered_mass(mass,
                      radius_outer,
                      radius_center,
                      density):
    """Calculate cell-centered enclosed mass

    Returns: np.array

    parameters
    ----------
    mass : []
        cell-outer enclosed mass (Msun)
    radius_outer : []
        cell-outer radius (cm)
    radius_center : []
        cell-center radius (cm)
    density : []
        cell-average density (g/cm^3)
    """
    mass = np.array(mass)
    radius = np.array(radius_outer)

    # cell-inner radius
    radius_inner = np.zeros(len(radius))
    radius_inner[1:] = radius[:-1]

    # cell-inner enclosed mass
    mass_inner = np.zeros(len(mass))
    mass_inner[1:] = mass[:-1]

    # left-half mass of cell
    vol_lhalf = 4/3 * np.pi * (radius_center**3 - radius_inner**3)
    mass_lhalf = vol_lhalf * density * g_to_msun

    mass_center = mass_inner + mass_lhalf

    return mass_center


def get_centered_radius(radius_outer):
    """Calculate cell-centered radius from cell-outer radius

    Returns: np.array

    parameters
    ----------
    radius_outer : []
        cell-outer radius
    """
    radius_outer = np.array(radius_outer)

    dr = np.array(radius_outer)
    dr[1:] = np.diff(dr)  # cell width

    r_center = radius_outer - (0.5 * dr)

    return r_center


def get_xi(mass, radius):
    """Calculate compactness parameter

    Returns: np.array

    parameters
    ----------
    mass : []
        Enclosed mass coordinate (Msun)
    radius : []
        radius coordinate (cm)
    """
    mass = np.array(mass)
    radius = np.array(radius)

    xi = mass / (radius * cm_to_1k_km)

    return xi


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


def get_velz(radius, ang_velocity):
    """Calculate tangential velocity (velz) from angular verlocity

    Returns: np.array
        tangential velocity [cm/s]

    parameters
    ----------
    radius : []
        radius coordinate (cm)
    ang_velocity : []
        angular velocity [rad/s]
    """
    radius = np.array(radius)
    ang_velocity = np.array(ang_velocity)

    velz = radius * ang_velocity

    return velz
