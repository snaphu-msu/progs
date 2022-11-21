import numpy as np
from astropy import constants as const
from astropy import units

# progs
from . import paths
from . import io
from . import configuration
from . import network
from . import plotting
from . import tools

msun_to_g = units.M_sun.to(units.g)

"""
Class for handling a given progenitor model
"""


class ProgModel:
    """
    Object representing a core-collapse progenitor model

    attributes
    ----------
    composition : pd.DataFrame
        subset of table containing only network species abundances (mass fraction)
    config : dict
        Progenitor-specific parameters loaded from 'config/<set_name>.ini'
    filename : str
        Name of raw progenitor file
    filepath : str
        Path to raw progenitor file
    mass : int or float
        Stellar mass (in Msun) of progenitor model.
    network : [str]
        table of network isotopes used
    set_name : str
        Name of progenitor set, e.g. 'sukhbold_2016'.
    sums : dict
        summed composition quantities (e.g. sumx, sumy, ye)
    table : pd.DataFrame
        Main table of radial profile parameters, including composition
    """

    def __init__(self,
                 mass,
                 set_name):
        """
        parameters
        ----------
        mass : float/int
            Stellar mass (in Msun) of progenitor model.
            Precision needs to match the file label
                e.g. mass=12.1 for 's12.1_presn',
                     mass=60 for 's60_presn'
        set_name : str
            Name of progenitor set, e.g. 'sukhbold_2016'
        """
        self.mass = mass
        self.set_name = set_name

        self.filename = paths.prog_filename(mass, set_name=set_name)
        self.filepath = paths.prog_filepath(mass, set_name=set_name)
        self.config = configuration.load_config(set_name)

        self.table = io.load_prog(mass, set_name, config=self.config)

        network_name = self.config['network']['name']
        self.network = network.load_network(network_name)
        self.composition = self.table[self.network.isotope]
        self.sums = network.get_sums(self.composition, self.network)

    # =======================================================
    #                      Quantities
    # =======================================================    
    def get_compactness(self, mass=2.5):
        """Compute the compactness xi = (M/Msun) / (R(M) / 1000km)

        parameters
        ----------
        mass : float
            mass parameter [Msun], typically 1.75 or 2.5
        """
        cm_to_1k_km = units.cm.to(1000 * units.km)

        idx = tools.find_nearest_idx(self.table['mass'], mass * msun_to_g)
        radius = self.table['radius'][idx]

        xi = mass / (radius * cm_to_1k_km)

        return xi

    def get_luminosity(self):
        """Return 4piR^2 sigma_sb T^4
        """
        sb = const.sigma_sb.cgs.value

        radius = self.table['radius'].iloc[-1]
        temperature = self.table['temperature'].iloc[-1]

        lum = 4.0 * np.pi * radius**2 * sb * temperature**4

        return lum

    # =======================================================
    #                      Plotting
    # =======================================================
    def plot_multi(self,
                   y_vars,
                   x_var='radius',
                   y_scale=None,
                   x_scale=None,
                   max_cols=1,
                   sub_figsize=(8, 6),
                   legend=False):
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
        fig, ax = plotting.setup_subplots(n_var,
                                          max_cols=max_cols,
                                          sub_figsize=sub_figsize,
                                          squeeze=False)

        for i, y_var in enumerate(y_vars):
            row = int(np.floor(i / max_cols))
            col = i % max_cols

            self.plot(y_var=y_var,
                      x_var=x_var,
                      y_scale=y_scale,
                      x_scale=x_scale,
                      ax=ax[row, col],
                      legend=legend if i == 0 else False)
        return fig

    def plot(self,
             y_var,
             x_var='radius',
             y_scale=None,
             x_scale=None,
             ax=None,
             legend=False,
             title=True,
             ylims=None,
             xlims=None,
             figsize=(8, 6),
             label=None,
             linestyle='-',
             marker=''):
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

        ax.plot(self.table[x_var],
                self.table[y_var],
                ls=linestyle,
                marker=marker,
                label=label)

        return fig

    def _set_ax_title(self, ax, title):
        """Add title to axis if title==True

        parameters
        ----------
        ax : Axis
        title : bool
        """
        if title:
            string = f'{self.set_name}: {self.filename}'
            plotting.set_ax_title(ax=ax, string=string, title=title)
