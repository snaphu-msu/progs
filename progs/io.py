import os
import pandas as pd
from astropy import units

# progs
from . import paths
from . import configuration

g_to_msun = units.g.to(units.M_sun)
cm_to_1k_km = units.cm.to(1e3 * units.km)


def load_prog(mass,
              set_name,
              config=None):
    """Load progenitor model from file

    parameters
    ----------
    mass : float/int
    set_name : str
    config : {}
    """
    config = configuration.check_config(config=config, set_name=set_name)
    raw = load_raw(mass, set_name, config=config)
    prog = pd.DataFrame()

    for key, idx in config['columns'].items():
        prog[key] = pd.to_numeric(raw[idx], errors='ignore')

    add_derived_columns(prog, config=config)

    return prog


def load_raw(mass,
             set_name,
             config=None):
    """Load raw progenitor model from file

    parameters
    ----------
    mass : float/int
    set_name : str
    config : {}
    """
    config = configuration.check_config(config, set_name=set_name)
    filepath = paths.prog_filepath(mass, set_name)

    delim_whitespace = config['load']['delim_whitespace']
    skiprows = config['load']['skiprows']
    missing_char = config['load']['missing_char']

    raw = pd.read_csv(filepath,
                      delim_whitespace=delim_whitespace,
                      skiprows=skiprows,
                      header=None)

    raw = raw.replace(missing_char, 0.0)

    return raw


def add_derived_columns(table, 
                        config):
    """Add derived column variables to table
    
    parameters
    ----------
    table : pd.DataFrame
    config : {}
    """
    derived_cols = config['load']['derived_columns']

    if 'compactness' in derived_cols:
        add_compactness(table)


def add_compactness(table):
    """Adds compactness column to prog table

    parameters
    ----------
    table : pd.DataFrame
    """
    if ('radius' not in table) or ('mass' not in table):
        raise ValueError(f'Need radius and mass columns to calculate compactness')

    table['compactness'] = (table['mass'] * g_to_msun) / (table['radius'] * cm_to_1k_km)


def find_progs(set_name,
               config=None):
    """Find all available progenitor models in a set

    Returns : [str]
        list of masses

    parameters
    ----------
    set_name : str
    config : {}
    """
    config = configuration.check_config(config=config, set_name=set_name)
    path = paths.set_path(set_name)

    progs = []
    filelist = os.listdir(path)

    for filename in filelist:
        if config['load']['match_str'] in filename:
            mass = filename.strip(config['load']['strip'])
            progs += [mass]

    progs = sorted(progs, key=float)

    return progs
