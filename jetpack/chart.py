"""
Chart
-----

Tools for making nice and readable plots using matplotlib

"""

# imports
import numpy as np
import matplotlib.pyplot as plt
from functools import wraps

__all__ = ['plotwrapper',  'image', 'hist', 'hist2d', 'errorplot',
           'setfontsize', 'noticks', 'nospines', 'breathe']


def plotwrapper(fun):
    """
    Decorator that adds sane plotting defaults to the kwargs of a function
    """

    @wraps(fun)
    def wrapper(*args, **kwargs):

        if 'ax' not in kwargs:

            if 'fig' not in kwargs:
                kwargs['fig'] = plt.figure()

            kwargs['ax'] = kwargs['fig'].add_subplot(111)

        else:

            if 'fig' not in kwargs:
                kwargs['fig'] = kwargs['ax'].get_figure()

        res = fun(*args, **kwargs)
        plt.show()
        plt.draw()
        return res

    return wrapper


def axwrapper(fun):
    """
    Decorator that adds axis arguments, used for functions that modify
    and existing plot (this decorator will never create a new plot)
    """

    @wraps(fun)
    def wrapper(*args, **kwargs):

        if 'ax' not in kwargs:

            if 'fig' not in kwargs:
                kwargs['fig'] = plt.gcf()

            kwargs['ax'] = plt.gca()

        else:

            if 'fig' not in kwargs:
                kwargs['fig'] = kwargs['ax'].get_figure()

        res = fun(*args, **kwargs)
        plt.show()
        plt.draw()
        return res

    return wrapper


@plotwrapper
def image(img, mode='div', center=True, cmap=None, aspect='equal', vmin=None, vmax=None, **kwargs):
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
        A matplotlib colormap to use (default: 'seismic' for 'div', 'gray' for 'seq')

    aspect : string, optional
        Same as in plt.imshow, either 'equal' or 'auto'

    ax : matplotlib axes handle, optional
        A handle to a matplotlib axes to use for plotting

    """

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
            vmin = img_max
        if vmax is None:
            vmax = img_max
        if cmap is None:
            cmap = 'gray'
    else:
        raise ValueError("Unrecognized mode: '" + mode + "'")

    # make the image
    kwargs['ax'].imshow(img, cmap=cmap, interpolation=None,
                        vmin=vmin, vmax=vmax, aspect=aspect)

    # clear ticks
    noticks(ax=kwargs['ax'])

    # display
    plt.show()
    plt.draw()


@plotwrapper
def corrplot(C, cmap=None, cmap_range=(0.,1.), cbar=True, fontsize=14, **kwargs):
    """
    Plots values in a correlation matrix

    """

    ax = kwargs['ax']
    n = len(C)

    # defaults
    if cmap is None:
        if min(cmap_range) >= 0:
            cmap = "OrRd"
        elif max(cmap_range) <= 0:
            cmap = "RdBu"
        else:
            cmap = "gray"

    # remove values
    rr, cc = np.triu_indices(n, k=1)
    C[rr, cc] = np.nan

    vmin, vmax = cmap_range
    img = ax.imshow(C, cmap=cmap, vmin=vmin, vmax=vmax, aspect='equal')

    if cbar:
        plt.colorbar(img) #, shrink=0.75)

    for j in range(n):
        for i in range(j+1,n):
            ax.text(i, j, '{:0.2f}'.format(C[i,j]), fontsize=fontsize,
                    fontdict={'ha': 'center', 'va': 'center'})

    noticks(ax=ax)


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
def errorplot(x, y, ye, color='k', xscale='linear', fmt='-', **kwargs):
    """
    Plot a line with error bars

    """

    ax = kwargs['ax']
    ax.plot(x, y, fmt, color=color)
    ax.plot(x, y+ye, '+')
    ax.plot(x, y-ye, '+')
    for i, xi in enumerate(x):
        ax.plot(np.array([xi, xi]), np.array([y[i]-ye[i], y[i]+ye[i]]), '-',
                color=color, linewidth=4)

    ax.set_xscale(xscale)

    return ax


@plotwrapper
def setfontsize(size=18, **kwargs):
    """
    Sets the font size of the x- and y- tick labels of the current axes

    Parameters
    ----------
    size : int
        The font size to use

    """

    ax = kwargs['ax']
    ax.set_xticklabels(ax.get_xticks(), fontsize=size)
    ax.set_yticklabels(ax.get_yticks(), fontsize=size)


@axwrapper
def noticks(**kwargs):
    """
    Clears tick marks (useful for images)
    """

    ax = kwargs['ax']
    ax.set_xticks([])
    ax.set_yticks([])
    return ax


@axwrapper
def nospines(**kwargs):
    """
    Hides the top and rightmost axis spines
    """

    ax = kwargs['ax']

    # disable spines
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # disable ticks
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    return ax


@axwrapper
def breathe(factor=0.05, **kwargs):
    ax = kwargs['ax']

    if ax.spines['bottom'].get_bounds():
        xa, xb = ax.spines['bottom'].get_bounds()
    else:
        xa, xb = ax.get_xlim()

    xrng = xb - xa
    ax.set_xlim(xa - factor * xrng, xb + factor * xrng)
    ax.spines['bottom'].set_bounds(xa, xb)

    if ax.spines['left'].get_bounds():
        ya, yb = ax.spines['left'].get_bounds()
    else:
        ya, yb = ax.get_ylim()

    yrng = yb - ya
    ax.set_ylim(ya - factor * yrng, yb + factor * yrng)
    ax.spines['left'].set_bounds(ya, yb)

    nospines(**kwargs)
    return ax
