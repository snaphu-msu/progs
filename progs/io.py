import os
import subprocess
import numpy as np
import pandas as pd
import ast
from astropy import units
from configparser import ConfigParser

# progs
from . import quantities

g_to_msun = units.g.to(units.M_sun)


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
    progs = []
    config = check_config(config=config, progset_name=progset_name)
    progfiles = find_prog_files(progset_name, config=config)

    for filename in progfiles:
        zams = filename.strip(config['load']['strip'])
        progs += [zams]

    progs = sorted(progs, key=float)

    return progs


def find_prog_files(progset_name,
                    config=None):
    """Find all available progenitor model files in a set

    Returns : [str]
        list of progenitor filenames

    parameters
    ----------
    progset_name : str
    config : {}
    """
    config = check_config(config=config, progset_name=progset_name)
    path = progset_path(progset_name)

    progfiles = []
    filelist = os.listdir(path)

    for filename in filelist:
        if config['load']['match_str'] in filename:
            progfiles += [filename]

    return progfiles


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
#                 Profile files
# =======================================================
def load_profile(zams,
                 progset_name,
                 filepath=None,
                 config=None):
    """Load progenitor model from file
    
    Returns : pd.DataFrame
    
    parameters
    ----------
    zams : str
    progset_name : str
    filepath : str
    config : {}
    """
    profile = extract_profile(zams=zams,
                              progset_name=progset_name,
                              filepath=filepath,
                              config=config)

    return profile


def extract_profile(zams,
                    progset_name,
                    filepath=None,
                    config=None):
    """Extract progenitor profile from file

    Returns : pd.DataFrame

    parameters
    ----------
    zams : str
    progset_name : str
    filepath : str
    config : {}
    """
    config = check_config(config=config, progset_name=progset_name)
    raw = load_raw_table(zams, progset_name, filepath=filepath, config=config)
    profile = pd.DataFrame()

    for key, idx in config['columns'].items():
        profile[key] = pd.to_numeric(raw[idx], errors='ignore')

    profile['mass'] = profile['mass'] * g_to_msun
    add_derived_columns(profile, config=config)

    return profile


def load_raw_table(zams,
                   progset_name,
                   filepath=None,
                   config=None):
    """Load unformatted progenitor model from file

    Returns : pd.DataFrame
    
    parameters
    ----------
    zams : str
    progset_name : str
    filepath : str
    config : {}
    """
    config = check_config(config, progset_name=progset_name)

    if filepath is None:
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


def save_profile_cache(profile,
                       zams,
                       progset_name):
    """Save profile table to cached file

    parameters
    ----------
    profile : pd.DataFrame
    zams : str
    progset_name : str
    """
    filepath = profile_cache_filepath(zams, progset_name)
    path = os.path.split(filepath)[0]
    check_mkdir(path)

    profile.to_pickle(filepath, compression=None)


def load_profile_cache(zams,
                       progset_name):
    """Save profile table to cached file

    parameters
    ----------
    zams : str
    progset_name : str
    """
    filepath = profile_cache_filepath(zams, progset_name)
    profile = pd.read_pickle(filepath)

    return profile


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

    if 'mass' in derived_cols:
        add_enclosed_mass(profile)

    if 'compactness' in derived_cols:
        add_compactness(profile)

    if 'luminosity' in derived_cols:
        add_luminosity(profile)

    if 'shells' in derived_cols:
        add_shells(profile, shell_isotopes=config['load']['shells'])


def add_enclosed_mass(profile):
    """Add enclosed mass column to profile
        Assumes existing 'mass' column is zone mass

    parameters
    ----------
    profile : pd.DataFrame
    """
    if 'mass' not in profile:
        raise ValueError(f'Need mass column to calculate enclosed mass')

    profile['mass'] = quantities.get_enclosed_mass(zone_mass=profile['mass'])


def add_compactness(profile):
    """Add compactness column to profile

    parameters
    ----------
    profile : pd.DataFrame
    """
    if ('radius' not in profile) or ('mass' not in profile):
        raise ValueError(f'Need radius and mass columns to calculate compactness')

    profile['compactness'] = quantities.get_compactness(mass=profile['mass'],
                                                        radius=profile['radius'])


def add_luminosity(profile):
    """Add blackbody luminosity column to profile

    parameters
    ----------
    profile : pd.DataFrame
    """
    if ('radius' not in profile) or ('temperature' not in profile):
        raise ValueError(f'Need radius and temperature columns to calculate luminosity')

    profile['luminosity'] = quantities.get_luminosity(radius=profile['radius'],
                                                      temperature=profile['temperature'])


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
    path = os.path.abspath(path)

    return path


def config_filepath(progset_name):
    """Return path to config file

    Returns : str

    parameters
    ----------
    progset_name : str
    """
    filepath = os.path.join(top_path(), 'progs', 'config', f'{progset_name}.ini')
    filepath = os.path.abspath(filepath)

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
    config = load_config(progset_name)
    progfiles = find_prog_files(progset_name)

    filename = None

    for file in progfiles:
        if file.strip(config['load']['strip']) == zams:
            filename = file

    if filename is None:
        raise ValueError(f"zams='{zams}' not found in progset '{progset_name}'")

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


def profile_cache_filepath(zams, progset_name):
    """Return filepath to cached profile table

    Returns : str

    parameters
    ----------
    zams : str
    progset_name : str
    """
    filename = f'profile_{progset_name}_{zams}.pickle'
    filepath = os.path.join(top_path(), 'temp', 'profile', filename)

    return filepath


def check_mkdir(path):
    """Create path directory(s) if not present

    parameters
    ----------
    path : str
    """
    if not os.path.exists(path):
        subprocess.run(['mkdir', '-p', path], check=True)
