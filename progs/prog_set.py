# progs
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
        self.masses = io.find_progs(set_name)

        self.progs = {}
        self.load_progs()

    def load_progs(self):
        """Load all progenitor models
        """
        for mass in self.masses:
            print(f'\rLoading mass: {mass}  ', end='')

            self.progs[mass] = ProgModel(mass=mass,
                                         set_name=self.set_name,
                                         config=self.config)
