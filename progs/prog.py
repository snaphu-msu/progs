import numpy as np

# progs
from . import paths
from . import load_save
from . import configuration
from . import network
from . import plotting
from . import tools

from astropy import constants as const

"""
Class for handling a given progenitor model
"""


class Prog:
    """Prog
    Object representing a particular core-collapse progenitor model

    attributes
    ----------
    composition : pd.DataFrame
        subset of table containing only network species abundances (mass fraction)
    config : dict
        Progenitor-specific parameters loaded from 'config/[series].ini'
    filename : str
        Name of raw progenitor file
    filepath : str
        Path to raw progenitor file
    mass : int or float
        Stellar mass (in Msun) of progenitor model.
    network : [str]
        table of network isotopes used
    series : str
        Name of progenitor series/set, e.g. 'sukhbold_2016'.
    sums : dict
        summed composition quantities (e.g. sumx, sumy, ye)
    table : pd.DataFrame
        Main table of radial profile parameters, including composition
    verbose : bool
        Print output or not
    """

    def __init__(self, mass, series, verbose=True):
        """
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
        """
        self.mass = mass
        self.series = paths.check_alias(series)
        self.verbose = verbose

        self.filename = paths.prog_filename(mass, series=series)
        self.filepath = paths.prog_filepath(mass, series=series)
        self.config = configuration.load_config(series, verbose)

        self.table = load_save.load_prog(mass, series, config=self.config,
                                         verbose=verbose)

        network_name = self.config['network']['name']
        self.network = network.load_network(network_name)
        self.composition = self.table[self.network.isotope]
        self.sums = network.get_sums(self.composition, self.network)


    # =======================================================
    #                      Quantities
    # =======================================================    

    def get_compactness(self, mass=2.5):
        """
        Compute the compactness xi = (M/Msun) / (R(M) / 1000km)

        parameters:
        -----------
        mass : float"""

        # just make sure the units are right.
        if (mass > 1000.0 ):
            mass /= const.M_sun.cgs.value

        ind = np.max( np.where( self.table['mass']/const.M_sun.cgs.value <= mass) )
        r = self.table['radius'][ind]
        return mass /  (r / 1e8) 

    def get_luminosity(self):
        """
        Return 4piR^2 \sigma_sb T^4
        """
        sb = const.sigma_sb.cgs.value
        n = len(self.table['radius'])
        return 4.0 * np.pi * self.table['radius'][n-1]**2 * sb * self.table['temperature'][n-1]**4


    # =======================================================
    #                      Plotting
    # =======================================================
    def plot_multi(self, y_vars, x_var='radius', y_scale=None, x_scale=None,
                   max_cols=1, sub_figsize=(8, 6), legend=False):
        """Plot one or more profile variables

        parameters
        ----------
        y_vars : str or [str]
            column(s) from self.table to plot on y-axis
        x_var : str
            variable to plot on x-axis
        y_scale : {'log', 'linear'}
        x_scale : {'log', 'linear'}
        legend : bool
        max_cols : bool
        sub_figsize : tuple
        """
        y_vars = tools.ensure_sequence(y_vars)
        n_var = len(y_vars)
        fig, ax = plotting.setup_subplots(n_var, max_cols=max_cols,
                                          sub_figsize=sub_figsize, squeeze=False)

        for i, y_var in enumerate(y_vars):
            row = int(np.floor(i / max_cols))
            col = i % max_cols

            self.plot(y_var=y_var, x_var=x_var, y_scale=y_scale,
                      x_scale=x_scale, ax=ax[row, col],
                      legend=legend if i == 0 else False)
        return fig

    def plot(self, y_var, x_var='radius', y_scale=None, x_scale=None,
             ax=None, legend=False, title=True,
             ylims=None, xlims=None, figsize=(8, 6), label=None,
             linestyle='-', marker=''):
        """Plot given profile variable

        parameters
        ----------
        y_var : str
            variable to plot on y-axis (from Simulation.profile)
        x_var : str
            variable to plot on x-axis
        y_scale : {'log', 'linear'}
        x_scale : {'log', 'linear'}
        ax : Axes
        legend : bool
        title : bool
        ylims : [min, max]
        xlims : [min, max]
        figsize : [width, height]
        label : str
        linestyle : str
        marker : str
        """
        fig, ax = plotting.check_ax(ax=ax, figsize=figsize)
        plotting.set_ax_lims(ax=ax, ylims=ylims, xlims=xlims)
        plotting.set_ax_scales(ax=ax, y_scale=y_scale, x_scale=x_scale)
        plotting.set_ax_legend(ax=ax, legend=legend)
        self._set_ax_title(ax=ax, title=title)

        ax.plot(self.table[x_var], self.table[y_var], ls=linestyle,
                marker=marker, label=label)

        return fig

    def _set_ax_title(self, ax, title):
        """Add title to axis if title==True

        parameters
        ----------
        ax : Axis
        title : bool
        """
        if title:
            string = f'{self.series}: {self.filename}'
            plotting.set_ax_title(ax=ax, string=string, title=title)
