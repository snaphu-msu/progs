import numpy as np

# progs
from . import prog_io
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
    filepath : str
        Path to raw progenitor file
    zams : str
        ZAMS mass [Msun] of progenitor model
    network : [str]
        table of network isotopes used
    progset_name : str
        Name of progenitor set, e.g. 'sukhbold_2016'
    network_sums : dict
        quantities calculated from the network composition (sumx, sumy, ye, abar)
        NOTE: these can be inconsistent with the values in the progenitor file!
    profile : pd.DataFrame
        Table of all radial profile quantities, including composition
    """

    def __init__(self,
                 zams,
                 progset_name,
                 config=None,
                 reload=False,
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
        reload : bool
            force reload of profile, instead of loading cached table
        """
        self.zams = zams
        self.progset_name = progset_name
        self.label = f'{progset_name}: {zams} Msun'

        self.filepath = prog_io.prog_filepath(zams, progset_name=progset_name)
        self.config = prog_io.check_config(config=config, progset_name=progset_name)

        self.profile = prog_io.load_profile(zams,
                                            progset_name,
                                            filepath=self.filepath,
                                            config=self.config,
                                            reload=reload)

        self.network = prog_io.load_network(progset_name, config=self.config)
        self.composition = self.profile[self.network.isotope]
        self.network_sums = network.get_sums(self.composition, self.network)

        self.scalars = {}
        self.get_scalars()

    # =======================================================
    #                      Quantities
    # =======================================================
    def get_scalars(self):
        """Get scalar variables
        """
        surface = self.profile.iloc[-1]
        self.scalars['presn_mass'] = surface['mass_edge']
        self.scalars['presn_radius'] = surface['radius_edge']
        self.scalars['presn_temperature'] = surface['temperature']
        self.scalars['presn_luminosity'] = surface['luminosity']

        for xi_mass in self.config['scalars']['xi']:
            self.scalars[f'xi_{xi_mass}'] = self.get_xi(mass=xi_mass)

        self.get_cores()

    def get_cores(self):
        """Get core masses/radii from shell profiles
        """
        for name, iso in self.config['scalars']['core_transition'].items():
            threshold = self.config['scalars']['core_thresh'][name]
            shell = self.profile[self.profile[iso] > threshold]

            if len(shell) == 0:
                mass = self.scalars['presn_mass']
                radius = self.scalars['presn_radius']
            else:
                mass = shell.iloc[0]['mass']
                radius = shell.iloc[0]['radius']

            self.scalars[f'coremass_{name}'] = mass
            self.scalars[f'corerad_{name}'] = radius

    def get_xi(self, mass=2.5):
        """Get the compactness parameter xi = (M/Msun) / (R(M) / 1000km)

        Returns : float

        parameters
        ----------
        mass : float
            Mass coordinate [Msun], typically 1.75 or 2.5
        """
        xi = self.interpolate_profile(x=mass, y_var='xi', x_var='mass')
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
                         core_masses=True,
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
        core_masses : bool
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
                    self.profile[isotope],
                    ls=linestyle,
                    marker=marker,
                    label=isotope)

        if core_masses:
            for i, core in enumerate(self.config['scalars']['core_thresh']):
                ax.vlines(x=self.scalars[f'coremass_{core}'],
                          ymin=0,
                          ymax=1.2,
                          linestyle='--',
                          color=f'C{i}',
                          label=f'{core} core')

        plotting.set_ax_legend(ax=ax, legend=legend, loc=1)

        return fig

    def plot_multi(self,
                   y_vars,
                   x_var='mass',
                   y_scale=None,
                   x_scale=None,
                   marker=None,
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
        marker : str
        legend : bool
        max_cols : bool
        sub_figsize : tuple
        """
        y_vars = tools.ensure_sequence(y_vars)
        n_var = len(y_vars)
        fig, ax = plotting.setup_subplots(n_var,
                                          max_cols=max_cols,
                                          sub_figsize=sub_figsize,
                                          sharex=True,
                                          squeeze=False)

        for i, y_var in enumerate(y_vars):
            row = int(np.floor(i / max_cols))
            col = i % max_cols

            self.plot(y_var=y_var,
                      x_var=x_var,
                      y_scale=y_scale,
                      x_scale=x_scale,
                      marker=marker,
                      ax=ax[row, col],
                      legend=legend if i == 0 else False)
        return fig
