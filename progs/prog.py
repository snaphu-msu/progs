import numpy as np
import pandas as pd

# progs
from . import paths


class Prog:
    def __init__(self, mass, series):
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
        """
        self.mass = mass
        self.series = paths.check_alias(series)

        self.filename = paths.prog_filename(mass, series=series)
        self.filepath = paths.prog_filepath(mass, series=series)
