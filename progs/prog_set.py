import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib import colormaps as cm
from matplotlib.widgets import Slider

# progs
from . import io
from . import plotting
from . import tools
from . import network
from .prog_model import ProgModel


class ProgSet:
    """
    Object representing a complete set of progenitor models

    attributes
    ----------
    config : {}
        Progenitor-specific parameters loaded from 'config/<progset_name>.ini'
    network : [str]
        table of network isotopes used
    progs : {zams: ProgModel}
        Full set of progenitor model objects
    progset_name : str
        Name of progenitor set, e.g. 'sukhbold_2016'
    reload : bool
        Force reload of profiles, instead of loading cached tables
    scalars : pd.DataFrame
        Table of scalar values for all models
    xi : xr.Dataset
        Compactness parameter extracted over whole set
    zams : [flt]
        list of ZAMS masses
    """

    def __init__(self,
                 progset_name,
                 reload=False,
                 ):
        """
        parameters
        ----------
        progset_name : str
        reload : bool
        """
        self.progset_name = progset_name
        self.config = io.load_config(progset_name)
        self.reload = reload

        self.zams = None
        self.progs = {}
        self.scalars = pd.DataFrame()
        self.xi = None
        self.network = network.load_network(progset_name, config=self.config)

        self.load_progs()
        self.get_scalars()
        self.get_compactness()

    def load_progs(self):
        """Load all progenitor models
        """
        zams_list = io.find_progs(self.progset_name)

        for zams in zams_list:
            print(f'\rLoading progenitor: {zams} Msun    ', end='')

            self.progs[float(zams)] = ProgModel(zams=zams,
                                                progset_name=self.progset_name,
                                                config=self.config,
                                                reload=self.reload)

        self.zams = [float(x) for x in zams_list]
        print()

    # =======================================================
    #                      Quantities
    # =======================================================
    def get_scalars(self):
        """Extract table of progenitor scalars
        """
        self.scalars['zams'] = self.zams

        prog_0 = self.progs[self.zams[0]]
        scalars = {key: [] for key in prog_0.scalars}

        for prog in self.progs.values():
            for key in scalars:
                scalars[key] += [prog.scalars[key]]

        for key, scalar in scalars.items():
            self.scalars[key] = scalar

    def get_compactness(self):
        """Get table of compactness values
        """
        mass_grid = np.linspace(1.5, 3, 31)
        xi_set = {}

        for zams, prog in self.progs.items():
            prog_xi = xr.Dataset()
            prog_xi['xi'] = ('mass', prog.get_compactness(mass=mass_grid))
            prog_xi.coords['mass'] = mass_grid

            xi_set[zams] = prog_xi

        self.xi = xr.concat(xi_set.values(), dim='zams')
        self.xi.coords['zams'] = self.zams

    # =======================================================
    #                      Plotting
    # =======================================================
    def plot_scalars(self,
                     y_var,
                     x_var='zams',
                     y_scale=None,
                     x_scale=None,
                     ax=None,
                     legend=False,
                     title=True,
                     ylims=None,
                     xlims=None,
                     figsize=(8, 6),
                     label=None,
                     linestyle='none',
                     marker='.'):
        """Plot given scalar variable over full progenitor set

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
        plotting.set_ax_title(ax=ax, string=self.progset_name, title=title)
        plotting.set_ax_labels(ax=ax, x_var=x_var, y_var=y_var)

        ax.plot(self.scalars[x_var],
                self.scalars[y_var],
                ls=linestyle,
                marker=marker,
                label=label)

        plotting.set_ax_legend(ax=ax, legend=legend)

        return fig

    def plot_profiles(self,
                      y_var,
                      x_var='mass',
                      zams=None,
                      y_scale=None,
                      x_scale=None,
                      ax=None,
                      title=True,
                      ylims=None,
                      xlims=None,
                      figsize=(8, 6),
                      linestyle='-',
                      marker='',
                      colormap='viridis',
                      alpha=1,
                      legend=False,
                      ):
        """Plot stellar profiles over full progenitor set

        Returns : fig

        parameters
        ----------
        y_var : str
            variable to plot on y-axis (from Simulation.profile)
        x_var : str
            variable to plot on x-axis
        zams : []
            list of progenitors to plot, by zams mass. Defaults to all
        y_scale : {'log', 'linear'}
        x_scale : {'log', 'linear'}
        ax : Axes
        title : bool
        ylims : [min, max]
        xlims : [min, max]
        figsize : [width, height]
        linestyle : str
        marker : str
        colormap : str
        alpha : float
        legend : bool
        """
        fig, ax = plotting.check_ax(ax=ax, figsize=figsize)
        plotting.set_ax_lims(ax=ax, ylims=ylims, xlims=xlims)
        plotting.set_ax_scales(ax=ax, y_scale=y_scale, x_scale=x_scale)
        plotting.set_ax_title(ax=ax, string=self.progset_name, title=title)
        plotting.set_ax_labels(ax=ax, x_var=x_var, y_var=y_var)

        if zams is None:
            zams = self.zams
        else:
            zams = tools.ensure_sequence(zams)

        for mass in zams:
            prog = self.progs[mass]
            color_scale = mass / (0.5 * np.ptp(self.zams))
            color = cm[colormap](color_scale, alpha=alpha)

            ax.plot(prog.profile[x_var],
                    prog.profile[y_var],
                    ls=linestyle,
                    marker=marker,
                    color=color,
                    label=mass)

        plotting.set_ax_legend(ax=ax, legend=legend)

        return fig

    def plot_xi_slider(self,
                       y_var,
                       xi_0=2.5,
                       ):
        """Plot slider over compactness parameter
        """
        def update_slider(mass):
            xi = self.xi.sel(mass=mass)
            ax.lines[0].set_xdata(xi['xi'])
            fig.canvas.draw_idle()

        mass_grid = self.xi['mass'].values

        fig = plt.figure()
        ax = fig.add_axes([0.1, 0.2, 0.8, 0.65])
        slider_ax = fig.add_axes([0.1, 0.05, 0.8, 0.05])

        slider = Slider(slider_ax,
                        'M',
                        mass_grid[0],
                        mass_grid[-1],
                        valinit=xi_0,
                        valstep=0.05)

        ax.set_xlim([self.xi['xi'].min()-0.1, self.xi['xi'].max()+0.1])

        ax.plot(self.xi.sel(mass=xi_0)['xi'],
                self.scalars[y_var],
                marker='.',
                ls='none')

        slider.on_changed(update_slider)

        return slider
