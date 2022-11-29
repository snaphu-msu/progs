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
                 progset_name):
        """
        parameters
        ----------
        progset_name : str
        """
        self.progset_name = progset_name
        self.config = configuration.load_config(progset_name)

        self.zams = None
        self.progs = {}
        self.scalars = pd.DataFrame()

        self.load_progs()
        self.get_scalars()

    def load_progs(self):
        """Load all progenitor models
        """
        zams_list = io.find_progs(self.progset_name)

        for zams in zams_list:
            print(f'\rLoading progenitor: {zams} Msun    ', end='')

            self.progs[float(zams)] = ProgModel(zams=zams,
                                                progset_name=self.progset_name,
                                                config=self.config)

        self.zams = [float(x) for x in zams_list]
        print()

    def get_scalars(self):
        """Extract table of progenitor scalars
        """
        self.scalars['zams'] = self.zams

        scalars = {key: [] for key in self.config['load']['scalars']}

        for prog in self.progs.values():
            for key in scalars:
                scalars[key] += [prog.scalars[key]]

        for key, scalar in scalars.items():
            self.scalars[key] = scalar
