# -*- coding: utf-8 -*-
"""
Plots
"""
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np

from .utils import nospines, noticks, plotwrapper, setfontsize, tickdir

__all__ = ['hist', 'hist2d', 'errorplot', 'corrplot', 'bars', 'lines']


@plotwrapper
def hist(*args, **kwargs):
    """
    Wrapper for matplotlib.hist function

    """

    # remove kwargs that are filled in manually
    kwargs.pop('alpha', None)
    kwargs.pop('histtype', None)
    kwargs.pop('normed', None)

    # get the axis and figure handles
    ax = kwargs.pop('ax')
    kwargs.pop('fig')

    return ax.hist(*args, histtype='stepfilled', alpha=0.85,
                   normed=True, **kwargs)


@plotwrapper
def hist2d(x, y, bins=None, range=None, cmap='hot', **kwargs):
    """
    Function for visualizing a 2D histogram by binning given data

    Parameters
    ----------
    x : array_like
        The x-value of the data points to bin

    y : array_like
        The y-value of the data points to bin

    bins : array_like, optional
        Either the number of bins to use in each dimension, or the actual bin
        edges to use

    cmap : string
        A matplotlib colormap to use when generating the plot

    """

    # parse inputs
    if range is None:
        range = np.array([[np.min(x), np.max(x)], [np.min(y), np.max(y)]])

    if bins is None:
        bins = 25

    # compute the histogram
    cnt, xe, ye = np.histogram2d(x, y, bins=bins, normed=True, range=range)

    # generate the plot
    ax = kwargs['ax']
    ax.pcolor(xe, ye, cnt.T, cmap=cmap)
    ax.set_xlim(xe[0], xe[-1])
    ax.set_ylim(ye[0], ye[-1])
    ax.set_aspect('equal')
    setfontsize()


@plotwrapper
def errorplot(x, y, yerr, method='patch', color='k', xscale='linear', fmt='-',
              alpha_fill=0.3, **kwargs):
    """Plot a line with error bars"""

    ax = kwargs['ax']

    if np.isscalar(yerr) or len(yerr) == len(y):
        ymin = y - yerr
        ymax = y + yerr
    elif len(yerr) == 2:
        ymin, ymax = yerr
    else:
        raise ValueError('Invalid yerr value: ', yerr)

    if method is 'line':
        ax.plot(x, y, fmt, color=color, linewidth=4)
        ax.plot(x, ymax, '_', ms=20, color=color)
        ax.plot(x, ymin, '_', ms=20, color=color)
        for i, xi in enumerate(x):
            ax.plot(np.array([xi, xi]), np.array([ymin[i], ymax[i]]), '-',
                    color=color, linewidth=2)

    elif method is 'patch':
        ax.fill_between(x, ymin, ymax, color=color, alpha=alpha_fill, interpolate=True)
        ax.plot(x, y, fmt, color=color)

    else:
        raise ValueError("Method must be 'line' or 'patch'")

    ax.set_xscale(xscale)


@plotwrapper
def corrplot(C, cmap=None, cmap_range=(0.0, 1.0), cbar=True, fontsize=14, **kwargs):
    """
    Plots values in a correlation matrix

    """
    C = C.copy()
    ax = kwargs['ax']
    n = len(C)

    # defaults
    if cmap is None:
        if min(cmap_range) >= 0:
            cmap = "OrRd"
        elif max(cmap_range) <= 0:
            cmap = "RdBu"
        else:
            cmap = "viridis"

    # remove values
    rr, cc = np.triu_indices(n, k=1)
    C[rr, cc] = np.nan

    vmin, vmax = cmap_range
    img = ax.imshow(C, cmap=cmap, vmin=vmin, vmax=vmax, aspect='equal')

    if cbar:
        plt.colorbar(img)

    for j in range(n):
        for i in range(j + 1, n):
            ax.text(i, j, '{:0.2f}'.format(C[i, j]), fontsize=fontsize,
                    fontdict={'ha': 'center', 'va': 'center'})

    noticks(ax=ax)


@plotwrapper
def bars(labels, data, color='#888888', width=0.7, err=None,
         capsize=5, capthick=2, **kwargs):
    """Plots values as a bar chart

    Parameters
    ----------
    labels : list or iterable of text labels
    data : list or iterable of numerical values to plot
    color : color of the bars (default: #888888)
    width : width of the bars (default: 0.7)
    err : list or iterable of error bar values (default: None)
    """
    ax = kwargs['ax']

    n = len(data)
    x = np.arange(n) + width
    if err is not None:
        err = np.vstack((np.zeros_like(err), err))

    ax.bar(x, data, width, color=color)

    if err is not None:
        caplines = ax.errorbar(x, data, err, capsize=capsize, capthick=capthick, fmt='none', marker=None, color=color)[1]
        caplines[0].set_markeredgewidth(0)

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    tickdir('out', ax=ax)

    nospines(ax=ax)
    ax.tick_params(axis='x', length=0)
    ax.spines['bottom'].set_color('none')
    ax.set_xlim((0, n + width))

    return ax


@plotwrapper
def lines(x, lines=None, cmap='viridis', **kwargs):
    if lines is None:
        lines = list(x)
        x = np.arange(len(lines[0]))

    else:
        lines = list(lines)

    colors = cm.__getattribute__(cmap)(np.linspace(0, 1, len(lines)))

    for line, color in zip(lines, colors):
        plt.plot(x, line, color=color)
