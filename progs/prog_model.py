import numpy as np

# progs
from . import paths
from . import io
from . import configuration
from . import network
from . import plotting
from . import tools


class ProgModel:
    """
    Object representing a core-collapse progenitor model

    attributes
    ----------
    composition : pd.DataFrame
        subset of profile containing only network species abundances (mass fraction)
    config : dict
        Progenitor-specific parameters loaded from 'config/<progset_name>.ini'
    filename : str
        Name of raw progenitor file
    filepath : str
        Path to raw progenitor file
    zams : str
        ZAMS mass [Msun] of progenitor model
    network : [str]
        table of network isotopes used
    progset_name : str
        Name of progenitor set, e.g. 'sukhbold_2016'
    sums : dict
        summed composition quantities (e.g. sumx, sumy, ye)
    profile : pd.DataFrame
        Table of all radial profile quantities, including composition
    """

    def __init__(self,
                 zams,
                 progset_name,
                 config=None,
                 ):
        """
        parameters
        ----------
        zams : str
            ZAMS mass [Msun] of progenitor model.
            Needs to match filename e.g.:
                - zams='12.1' for 's12.1_presn',
                - zams='60' for 's60_presn'
        progset_name : str
            Name of progenitor set, e.g. 'sukhbold_2016'
        config : {}
        """
        self.zams = zams
        self.progset_name = progset_name
        self.label = f'{progset_name}: {zams} Msun'

        self.filename = paths.prog_filename(zams, progset_name=progset_name)
        self.filepath = paths.prog_filepath(zams, progset_name=progset_name)

        self.config = configuration.check_config(config=config,
                                                 progset_name=progset_name)

        self.profile = io.load_profile(zams, progset_name, config=self.config)

        self.network = network.load_network(progset_name, config=self.config)
        self.composition = self.profile[self.network.isotope]
        self.sums = network.get_sums(self.composition, self.network)

        self.scalars = {}
        self.get_scalars()

    # =======================================================
    #                      Quantities
    # =======================================================
    def get_scalars(self):
        """Get scalar variables
        """
        surface = self.profile.iloc[-1]
        self.scalars['presn_mass'] = surface['mass']
        self.scalars['presn_radius'] = surface['radius']
        self.scalars['presn_luminosity'] = surface['luminosity']

        self.scalars['xi_1.75'] = self.get_compactness(mass=1.75)
        self.scalars['xi_2.5'] = self.get_compactness(mass=2.5)

        self.get_core_masses()

    def get_core_masses(self):
        """Get core masses from composition profiles
        """
        si_shell = self.profile[self.profile['si28'] > 0.2]

        self.scalars['coremass_fe'] = si_shell['mass'].min()

    def get_compactness(self, mass=2.5):
        """Get the compactness parameter xi = (M/Msun) / (R(M) / 1000km)

        Returns : float

        parameters
        ----------
        mass : float
            Mass coordinate [Msun], typically 1.75 or 2.5
        """
        xi = self.interpolate_profile(x=mass, y_var='compactness', x_var='mass')
        return xi

    def interpolate_profile(self,
                            x,
                            y_var,
                            x_var='mass'):
        """Interpolate profile quanitity at given mass/radius coordinate

        Returns : float

        parameters
        ----------
        x : float or [float]
        y_var : str
        x_var : 'mass' or 'radius'
        """
        if x_var not in ['mass', 'radius']:
            raise ValueError("interpolation x_var must be 'mass' or 'radius'")

        y = np.interp(x, self.profile[x_var], self.profile[y_var])

        return y

    # =======================================================
    #                      Plotting
    # =======================================================
    def plot(self,
             y_var,
             x_var='mass',
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

        Returns : fig

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
        plotting.set_ax_title(ax=ax, string=self.label, title=title)
        plotting.set_ax_labels(ax=ax, x_var=x_var, y_var=y_var)

        ax.plot(self.profile[x_var],
                self.profile[y_var],
                ls=linestyle,
                marker=marker,
                label=label)

        plotting.set_ax_legend(ax=ax, legend=legend)

        return fig

    def plot_composition(self,
                         isotopes=None,
                         x_var='mass',
                         y_scale='linear',
                         x_scale=None,
                         ax=None,
                         legend=True,
                         title=True,
                         ylims=(1e-4, 1.1),
                         xlims=None,
                         figsize=(8, 6),
                         linestyle='-',
                         marker=''):
        """Plot isotopic composition

        Returns : fig

        parameters
        ----------
        isotopes : [str] or 'all'
            defaults to isotopes sepecified in config.network.plot
            'all' plots every isotope in the network
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
        linestyle : str
        marker : str
        """
        fig, ax = plotting.check_ax(ax=ax, figsize=figsize)
        plotting.set_ax_lims(ax=ax, ylims=ylims, xlims=xlims)
        plotting.set_ax_scales(ax=ax, y_scale=y_scale, x_scale=x_scale)
        plotting.set_ax_title(ax=ax, string=self.label, title=title)
        plotting.set_ax_labels(ax=ax, x_var=x_var, y_var='$X_i$')

        if isotopes is None:
            isotopes = self.config['network']['plot']
        elif isotopes == 'all':
            isotopes = self.network['isotope']

        for isotope in isotopes:
            ax.plot(self.profile[x_var],
                    self.composition[isotope],
                    ls=linestyle,
                    marker=marker,
                    label=isotope)

        plotting.set_ax_legend(ax=ax, legend=legend)

        return fig

    def plot_multi(self,
                   y_vars,
                   x_var='mass',
                   y_scale=None,
                   x_scale=None,
                   max_cols=1,
                   sub_figsize=(8, 6),
                   legend=False):
        """Plot one or more profile variables

        Returns : fig

        parameters
        ----------
        y_vars : str or [str]
            column(s) from self.profile to plot on y-axis
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
