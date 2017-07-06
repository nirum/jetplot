# -*- coding: utf-8 -*-
"""
Stats
-----

Some canned routines for statistical visualizations
"""

import warnings

import matplotlib.pyplot as plt
import numpy as np
from .utils import plotwrapper, nospines

__all__ = ['paired_scatter', 'density2d']

DEFAULT_COLOR_CYCLE = [(0.4470588235294118, 0.6196078431372549, 0.807843137254902),
                       (1.0, 0.6196078431372549, 0.2901960784313726),
                       (0.403921568627451, 0.7490196078431373, 0.3607843137254902),
                       (0.9294117647058824, 0.4, 0.36470588235294116),
                       (0.6784313725490196, 0.5450980392156862, 0.788235294117647),
                       (0.6588235294117647, 0.47058823529411764, 0.43137254901960786),
                       (0.9294117647058824, 0.592156862745098, 0.792156862745098),
                       (0.6352941176470588, 0.6352941176470588, 0.6352941176470588),
                       (0.803921568627451, 0.8, 0.36470588235294116),
                       (0.42745098039215684, 0.8, 0.8549019607843137)]


@plotwrapper
def density2d(x, y, gridsize=25, nbins=20, ratio=4, cmap='magma_r', color='darkgray', **kwargs):
    ax = plt.subplot2grid((ratio, ratio), (1, 0), colspan=3, rowspan=(ratio - 1))
    ax_top = plt.subplot2grid((ratio, ratio), (0, 0), colspan=3)
    ax_right = plt.subplot2grid((ratio, ratio), (1, ratio - 1), rowspan=(ratio - 1))

    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()
    ax.hexbin(x, y, gridsize=gridsize, extent=(xmin, xmax, ymin, ymax), cmap=cmap)

    xv, xe = np.histogram(x, bins=nbins, range=(xmin, xmax), normed=True)
    xb = xe[:-1] + np.mean(np.diff(xe))
    ax_top.plot(xb, xv, '-', color=color)
    nospines(ax=ax_top, bottom=True, left=True)

    yv, ye = np.histogram(y, bins=nbins, range=(ymin, ymax), normed=True)
    yb = ye[:-1] + np.mean(np.diff(ye))
    ax_right.plot(yv, yb, '-', color=color)
    nospines(ax=ax_right, bottom=True, left=True)

    return ax, ax_top, ax_right


def paired_scatter(data, labels=None, axes=None, categories=None,
                   color_cycle=DEFAULT_COLOR_CYCLE,
                   tickpad=1, tickrotation=60,
                   scatter_kw=dict(), hist_kw=dict(),
                   **subplots_kw):
    """ Create a scatter plot matrix from the given data. 
        
        Note
        ----
        This code was modified from: https://gist.github.com/adrn/5301190

        Parameters
        ----------
        data : numpy.ndarray
            A numpy array containined the scatter data to plot. The data
            should be shape MxN where M is the number of dimensions and 
            with N data points.
        labels : numpy.ndarray (optional)
            A numpy array of length M containing the axis labels.
        axes : matplotlib Axes array (optional)
            If you've already created the axes objects, pass this in to
            plot the data on that.
        tickpad : int (optional)
            number of axis tick marks to drop from either side
        tickrotation : int, float (optional)
            sets the rotation of the x-tick labels (60 degrees by default)
        scatter_kw : dict (optional)
            A dictionary of keyword arguments to pass to the 
            matplotlib.pyplot.scatter function calls.
        hist_kw : dict (optional)
            A dictionary of keyword arguments to pass to the 
            matplotlib.pyplot.hist function calls.
        **subplots_kw
            Additional keyword arguments are passed to the
            matplotlib.pyplot.subplots call.
    """
        
    try:
        M,N = data.shape
        if M > N: raise ValueError()
    except ValueError: # too many values to unpack
        raise ValueError("Invalid data shape {0}. You must pass in an array of "
                         "shape (M, N) where N > M.".format(data.shape))
    
    if labels == None:
        labels = ['']*M
        
    fig, axes = plt.subplots(M, M, **subplots_kw)

    # parse keyword arguments
    def _reset_default(kw, key, val):
        kw[key] = val if not key in kw.keys() else kw[key]

    # set scatter keyword defaults
    sc_kw = scatter_kw.copy()
    _reset_default(sc_kw, "edgecolor", "none")
    _reset_default(sc_kw, "s", 10)

    # set hist keyword defaults
    h_kw = hist_kw.copy()
    _reset_default(h_kw, "histtype", "bar")
    _reset_default(h_kw, "stacked", True)
    if categories is None:
        _reset_default(h_kw, "color", "gray")

    # determine how to color the points
    if categories is not None:
        # override user-specified colors if categories are given.
        if "c" in sc_kw.keys():
            warnings.warn('Specifying categories overrides color option in scatter_kw.')
        
        # check that categories are input correctly
        if len(categories) != N:
            raise ValueError('categories must be a list with data.shape[1] elements')
        if isinstance(categories, list):
            categories = np.array(categories)
        # for cg in categories:
        #     if not isinstance(cg, int):
        #         raise ValueError('categories must be specified as a list of ints')
        
        # set the colors for the scatterplots
        catset = np.array(list(set(categories)))
        cols = [col for col, cg in zip(color_cycle, catset)]
        sc_kw["c"] = [cols[np.where(catset==cg)[0]] for cg in categories]
        h_kw["color"] = cols
    else:
        # black scatterpoints by default
        _reset_default(sc_kw, "c", "k")

    # Axes properties
    xmin = np.empty((M,M))
    xmax = np.empty((M,M))
    ymin = np.empty((M,M))
    ymax = np.empty((M,M))

    # First, go through and make plots
    for i in range(M):
        for j in range(M):
            # make plot
            if i == j:
                if categories is not None:
                    y = [data[i][categories == cg] for cg in set(categories)]
                else:
                    y = data[i]
                axes[i,i].hist(y, **h_kw)
            else:
                axes[i,j].scatter(data[j], data[i], **sc_kw)

            xmin[i,j], xmax[i,j] = axes[i,j].get_xlim()
            
            # ignore y-axes on histograms
            if i == j:
                ymin[i,j], ymax[i,j] = np.nan, np.nan
            else:
                ymin[i,j], ymax[i,j] = axes[i,j].get_ylim()
    
    # get axes limits for each row/col
    x0_ = np.min(xmin, axis=0)
    x1_ = np.max(xmax, axis=0)
    y0_ = np.nanmin(ymin, axis=1)
    y1_ = np.nanmax(ymax, axis=1)

    # Make a second pass over the plots to format axes
    for i, (y0, y1) in enumerate(zip(y0_, y1_)):
        for j, (x0, x1) in enumerate(zip(x0_, x1_)):

            # set x-axis limits
            axes[i,j].set_xlim([x0, x1])
            
            # don't change ylim for histograms
            if i != j:
                axes[i,j].set_ylim([y0, y1])
                
            # set spine color
            for spine in axes[i,j].spines.values():
                spine.set_color('gray')

            # y-axis formatting
            axes[i,j].yaxis.set_tick_params(direction='out')
            yt = axes[i,j].get_yticks()

            if j == 0 and i > 0:
                # format first column
                axes[i,j].set_ylabel(labels[i])
                axes[i,j].set_yticks([yt[tickpad], yt[-(tickpad+1)]])
                axes[i,j].yaxis.set_ticks_position('left')
            elif i == 0 and j == M-1:    
                # first row is special case
                axes[i,j].yaxis.set_ticks_position('right')
                axes[i,j].yaxis.set_label_position('right')
                axes[i,j].set_ylabel(labels[i])
                axes[i,j].set_yticks([yt[tickpad], yt[-(tickpad+1)]])
            else:
                axes[i,j].set_yticks([])

            # x-axis formatting
            axes[i,j].xaxis.set_tick_params(direction='out')
            xt = axes[i,j].get_xticks()

            if i == M-1:
                axes[i,j].set_xlabel(labels[j])
                axes[i,j].xaxis.set_ticks_position('bottom')
                axes[i,j].set_xticks([xt[tickpad], xt[-(tickpad+1)]])
                for tick in axes[i,j].get_xticklabels():
                    tick.set_rotation(tickrotation)
            else:
                axes[i,j].set_xticks([])

    fig.subplots_adjust(hspace=0.0, wspace=0.0, left=0.08, bottom=0.08, top=0.9, right=0.9)
    return fig, axes
