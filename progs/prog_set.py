# progs
import pandas as pd

from . import io
from . import configuration
from .prog_model import ProgModel


class ProgSet:
    """
    Object representing a complete set of progenitor models

    attributes
    ----------
    """

    def __init__(self,
                 set_name):
        """
        parameters
        ----------
        set_name : str
        """
        self.set_name = set_name
        self.config = configuration.load_config(set_name)

        self.zams = None
        self.progs = {}
        self.table = pd.DataFrame()

        self.load_progs()
        self.get_table()

    def load_progs(self):
        """Load all progenitor models
        """
        zams_list = io.find_progs(self.set_name)
        self.zams = [float(x) for x in zams_list]

        for zams in zams_list:
            print(f'\rLoading progenitor: {zams} Msun    ', end='')

            self.progs[zams] = ProgModel(zams=zams,
                                         set_name=self.set_name,
                                         config=self.config)
        print()

    def get_table(self):
        """Extract table of progenitor properties
        """
        self.table['zams'] = self.zams

        scalars = {key: [] for key in self.config['load']['scalars']}

        for prog in self.progs.values():
            for key in scalars:
                scalars[key] += [prog.scalars[key]]

        for key, scalar in scalars.items():
            self.table[key] = scalar
