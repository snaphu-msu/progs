import configparser
import os
import ast

# progs
from . import paths

"""
Module for handling configs for each progenitor set_name
"""


def load_config(set_name):
    """Load .ini config file and return as dict

    parameters
    ----------
    set_name : str
    """
    filepath = paths.config_filepath(set_name)

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


def check_config(config, set_name):
    """Check if config provided, load if not

    parameters
    ----------
    config : dict or None
    set_name : str
    """
    if config is None:
        config = load_config(set_name)

    return config
