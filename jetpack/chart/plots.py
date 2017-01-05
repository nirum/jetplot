# -*- coding: utf-8 -*-
"""
jetpack plots
"""
from .utils import plotwrapper, noticks, setfontsize
from functools import partial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

__all__ = ['hist', 'hist2d', 'errorplot', 'img', 'play', 'corrplot', 'imv']


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
def img(data, mode='div', center=True, cmap=None, aspect='equal', vmin=None, vmax=None, cbar=False, interpolation='none', **kwargs):
    """
    Visualize a matrix as an image

    Parameters
    ----------
    img : array_like
        The matrix to visualize

    mode : string, optional
        Either 'div' for a diverging image or 'seq' for sequential (default: 'div')

    center : boolean, optional
        Whether or not to mean-subtract the image

    cmap : string, optional
        A matplotlib colormap to use (default: 'seismic' for 'div', 'viridis' for 'seq')

    aspect : string, optional
        Same as in plt.imshow, either 'equal' or 'auto'

    ax : matplotlib axes handle, optional
        A handle to a matplotlib axes to use for plotting

    """

    # work with a copy of the original image data
    img = data.copy()

    # subtract off image mean
    if center:
        img -= np.mean(img)

    # image bounds
    img_min = np.min(img)
    img_max = np.max(img)
    abs_max = np.max(np.abs(img))

    if mode == 'div':
        if vmin is None:
            vmin = -abs_max
        if vmax is None:
            vmax = abs_max
        if cmap is None:
            cmap = 'seismic'
    elif mode == 'seq':
        if vmin is None:
            vmin = img_min
        if vmax is None:
            vmax = img_max
        if cmap is None:
            cmap = 'viridis'
    elif mode == 'cov':
        vmin, vmax, cmap, cbar = 0, 1, 'viridis', True
    elif mode == 'cov':
        vmin, vmax, cmap, cbar = -1, 1, 'seismic', True
    else:
        raise ValueError("Unrecognized mode: '" + mode + "'")

    # make the image
    kwargs['ax'].imshow(img, cmap=cmap, interpolation=interpolation,
                        vmin=vmin, vmax=vmax, aspect=aspect)

    # colorbar
    if cbar:
        plt.colorbar()

    # clear ticks
    noticks(ax=kwargs['ax'])


def play(images, cmap='gray', interval=100, clim=None, **kwargs):
    """Plays an animation of the given stack of images"""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    noticks(ax=ax)

    # set up the figure
    plt.axis('equal')
    img = ax.imshow(images[0])

    # set up the colormap
    img.set_cmap(cmap)
    img.set_interpolation('nearest')
    if clim is not None:
        img.set_clim(clim)
    else:
        maxval = np.max(np.abs(images))
        img.set_clim([-maxval, maxval])

    def animate(im):
        img.set_data(im)

    anim = animation.FuncAnimation(fig, animate, images, interval=interval)
    plt.show()
    return anim


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
def bars(*dicts, **kwargs):
    ax = kwargs['ax']
    raise NotImplementedError


# aliases
imv = partial(img, mode='seq')
