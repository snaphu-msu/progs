# progs
from . import paths
from . import load_save
from . import configuration
from . import network
"""
Class for handling a given progenitor model
"""


class Prog:
    def __init__(self, mass, series, verbose=True):
        """Object representing a single progenitor model

        parameters
        ----------
        mass : float/int
            Stellar mass (in Msun) of progenitor model.
            Precision needs to match the file label
                e.g. mass=12.1 for 's12.1_presn',
                     mass=60 for 's60_presn'
        series : str
            Name of progenitor series/set, e.g. 'sukhbold_2016'.
            Shorthand aliases may be defined, e.g. 's16' for 'sukhbold_2016'.
        verbose : bool


        attributes
        ----------
        mass : int or float
        series : str
        verbose : bool
        filename : str
        filepath : str
            Path to raw progenitor file
        config : dict
            Progenitor-specific parameters loaded from 'config/[series].ini'
        network : [str]
            table of network isotopes used
        table : pd.DataFrame
            Main table of radial profile parameters, including composition
        composition : pd.DataFrame
            subset of table containing only network species abundances (mass fraction)
        """
        self.mass = mass
        self.series = paths.check_alias(series)
        self.verbose = verbose

        self.filename = paths.prog_filename(mass, series=series)
        self.filepath = paths.prog_filepath(mass, series=series)
        self.config = configuration.load_config(series, verbose)

        network_name = self.config['network']['name']
        self.network = network.load_net(network_name)

        self.table = load_save.load_prog(mass, series, config=self.config,
                                         verbose=verbose)

        self.composition = self.table[self.network.isotope]
