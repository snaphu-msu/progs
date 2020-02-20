import configparser
import os
import ast

# progs
from . import paths
from .strings import printv

"""
Module for handling configs for each progenitor series
"""


def load_config(series, verbose=True):
    """Load .ini config file and return as dict

    parameters
    ----------
    series : str
    verbose : bool
    """
    filepath = paths.config_filepath(series)
    printv(f'Loading config: {filepath}', verbose)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f'Config file not found: {filepath}')

    ini = configparser.ConfigParser()
    ini.read(filepath)

    config = {}
    for section in ini.sections():
        config[section] = {}
        for option in ini.options(section):
            config[section][option] = ast.literal_eval(ini.get(section, option))

    return config


def get_column_list(config):
    """Return list of column names from a given config

    parameters
    ----------
    config : dict
    """
    params = list(config['param_columns'].keys())
    network = list(config['network_columns'].keys())

    return params + network
