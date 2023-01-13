import os
import numpy as np
import pandas as pd
from astropy import units
from astropy import constants as const
from configparser import ConfigParser
import ast


g_to_msun = units.g.to(units.M_sun)
cm_to_1k_km = units.cm.to(1e3 * units.km)


# =======================================================
#                 Files
# =======================================================
def find_progs(progset_name,
               config=None):
    """Find all available progenitor models in a set

    Returns : [str]
        list of ZAMS masses

    parameters
    ----------
    progset_name : str
    config : {}
    """
    config = check_config(config=config, progset_name=progset_name)
    path = progset_path(progset_name)

    progs = []
    filelist = os.listdir(path)

    for filename in filelist:
        if config['load']['match_str'] in filename:
            zams = filename.strip(config['load']['strip'])
            progs += [zams]

    progs = sorted(progs, key=float)

    return progs


# =======================================================
#                 Config files
# =======================================================
def load_config(progset_name):
    """Load .ini config file and return as dict

    Returns : {}

    parameters
    ----------
    progset_name : str
    """
    filepath = config_filepath(progset_name)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f'Config file not found: {filepath}')

    ini = ConfigParser()
    ini.read(filepath)

    config = {}
    for section in ini.sections():
        config[section] = {}
        for option in ini.options(section):
            config[section][option] = ast.literal_eval(ini.get(section, option))

    return config


def check_config(config, progset_name):
    """Check if config provided, load if not

    Returns : {}

    parameters
    ----------
    config : dict or None
    progset_name : str
    """
    if config is None:
        config = load_config(progset_name)

    return config


# =======================================================
#                 Loading tables
# =======================================================
def load_profile(zams,
                 progset_name,
                 config=None):
    """Load progenitor model from file
    
    Returns : pd.DataFrame
    
    parameters
    ----------
    zams : str
    progset_name : str
    config : {}
    """
    config = check_config(config=config, progset_name=progset_name)
    raw = load_raw_table(zams, progset_name, config=config)
    profile = pd.DataFrame()

    for key, idx in config['columns'].items():
        profile[key] = pd.to_numeric(raw[idx], errors='ignore')

    profile['mass'] = profile['mass'] * g_to_msun

    add_derived_columns(profile, config=config)

    return profile


def load_raw_table(zams,
                   progset_name,
                   config=None):
    """Load unformatted progenitor model from file

    Returns : pd.DataFrame
    
    parameters
    ----------
    zams : str
    progset_name : str
    config : {}
    """
    config = check_config(config, progset_name=progset_name)
    filepath = prog_filepath(zams, progset_name)

    delim_whitespace = config['load']['delim_whitespace']
    skiprows = config['load']['skiprows']
    missing_char = config['load']['missing_char']

    raw = pd.read_csv(filepath,
                      delim_whitespace=delim_whitespace,
                      skiprows=skiprows,
                      header=None)

    raw = raw.replace(missing_char, 0.0)

    return raw


# =======================================================
#                  Derived columns
# =======================================================
def add_derived_columns(profile,
                        config):
    """Add derived column variables to profile
    
    parameters
    ----------
    profile : pd.DataFrame
    config : {}
    """
    derived_cols = config['load']['derived_columns']

    if 'compactness' in derived_cols:
        add_compactness(profile)
    if 'luminosity' in derived_cols:
        add_luminosity(profile)
    if 'shells' in derived_cols:
        add_shells(profile, shell_isotopes=config['load']['shells'])


def add_compactness(profile):
    """Add compactness column to profile

    parameters
    ----------
    profile : pd.DataFrame
    """
    if ('radius' not in profile) or ('mass' not in profile):
        raise ValueError(f'Need radius and mass columns to calculate compactness')

    profile['compactness'] = profile['mass'] / (profile['radius'] * cm_to_1k_km)


def add_luminosity(profile):
    """Add blackbody luminosity column to profile

    parameters
    ----------
    profile : pd.DataFrame
    """
    if ('radius' not in profile) or ('temperature' not in profile):
        raise ValueError(f'Need radius and temperature columns to calculate luminosity')

    sb = const.sigma_sb.cgs.value
    radius = profile['radius']
    temp = profile['temperature']

    profile['luminosity'] = 4 * np.pi * sb * radius**2 * temp**4


def add_shells(profile, shell_isotopes):
    """Add combined shell compositions to profile

    parameters
    ----------
    profile : pd.DataFrame
    shell_isotopes : {name: [str]}
        grouped shell isotopes to combine
    """
    for shell_name, isotopes in shell_isotopes.items():
        shell = np.zeros(len(profile))

        for iso in isotopes:
            shell += profile[iso]

        profile[shell_name] = shell


# ===============================================================
#                      Paths
# ===============================================================
def top_path():
    """Return path to top-level repo directory

    Returns : str
    """
    path = os.path.join(os.path.dirname(__file__), '..')
    return path


def config_filepath(progset_name):
    """Return path to config file

    Returns : str

    parameters
    ----------
    progset_name : str
    """
    filepath = os.path.join(top_path(), 'progs', 'config', f'{progset_name}.ini')

    return filepath


def network_filepath(network):
    """Return path to profile of given network

    Returns : str

    parameters
    ----------
    network : str
    """
    filename = f'{network}.txt'
    filepath = os.path.join(top_path(), 'progs', 'networks', filename)

    return filepath


def prog_filename(zams, progset_name):
    """Return filename of progenitor

    Returns : str

    parameters
    ----------
    zams : str
    progset_name : str
    """
    filenames = {
        'sukhbold_2016': f's{zams}_presn',
    }

    filename = filenames.get(progset_name)

    if filename is None:
        raise ValueError(f"Progenitor set '{progset_name}' not defined")

    return filename


def prog_filepath(zams, progset_name):
    """Return filepath to progenitor model

    Returns : str

    parameters
    ----------
    zams : str
    progset_name : str
    """
    filename = prog_filename(zams, progset_name=progset_name)
    filepath = os.path.join(progset_path(progset_name), filename)

    return filepath


def progset_path(progset_name):
    """Return path to progenitor set directory

    Returns : str

    parameters
    ----------
    progset_name : str
    """
    path = os.path.join(top_path(), 'progenitor_sets', progset_name)
    return path
