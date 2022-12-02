import numpy as np
import pandas as pd
from matplotlib import colormaps as cm

# progs
from . import io
from . import configuration
from . import plotting
from . import tools
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
                      colormap='inferno',
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
