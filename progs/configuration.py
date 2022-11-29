import configparser
import os
import ast

# progs
from . import paths

"""
Module for handling config files for each progenitor set
"""


def load_config(progset_name):
    """Load .ini config file and return as dict

    Returns : {}

    parameters
    ----------
    progset_name : str
    """
    filepath = paths.config_filepath(progset_name)

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
