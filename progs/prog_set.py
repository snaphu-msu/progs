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

        self.progs = {}
        self.table = pd.DataFrame()

        self.load_progs()

    def load_progs(self):
        """Load all progenitor models
        """
        zams_list = io.find_progs(self.set_name)
        self.table['zams'] = [float(x) for x in zams_list]

        for zams in zams_list:
            print(f'\rLoading progenitor: {zams} Msun    ', end='')

            self.progs[zams] = ProgModel(zams=zams,
                                         set_name=self.set_name,
                                         config=self.config)
