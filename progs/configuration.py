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
    printv(f'Loading config: {os.path.abspath(filepath)}', verbose)

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


def check_config(config, series, verbose=True):
    """Check if config provided, load if not

    parameters
    ----------
    config : dict or None
    series : str
    verbose : bool
    """
    if config is None:
        config = load_config(series, verbose)

    return config
