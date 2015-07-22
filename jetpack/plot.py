"""
Tools for making nice and readable plots using matplotlib

"""

# imports
import numpy as np
import matplotlib.pyplot as plt
from functools import wraps

__all__ = ['plotwrapper',  'image', 'hist', 'hist2d', 'errorplot',
           'setfontsize']


def plotwrapper(fun):
    """
    Decorator that adds sane plotting defaults to the kwargs of a function
    """

    @wraps(fun)
    def wrapper(*args, **kwargs):

        if 'fig' not in kwargs:
            kwargs['fig'] = plt.figure()

        if 'ax' not in kwargs:
            kwargs['ax'] = kwargs['fig'].add_subplot(111)

        res = fun(*args, **kwargs)
        plt.show()
        plt.draw()
        return res

    return wrapper


@plotwrapper
def image(img, symmetric=True, colormap='seismic', **kwargs):
    """
    Visualize a matrix as an image

    Parameters
    ----------
    img : array_like
        The matrix to visualize

    symmetric : boolean, optional
        Whether or not to scale the colormap range so that it is symmetric
        about the image mean (Default: true).

    colormap : string, optional
        A matplotlib colormap to use (Default: 'seismic').

    ax : matplotlib axes handle, optional
        A handle to a matplotlib axes to use for plotting

    """

    # image mean
    mu = np.mean(img)

    # image bounds
    img_min = np.min(img - mu)
    img_max = np.max(img - mu)
    abs_max = np.max(np.abs(img - mu))
    vmin, vmax = (-abs_max, abs_max) if symmetric else (img_min, img_max)

    # make the image
    kwargs['ax'].imshow(img, cmap=colormap, interpolation=None,
                        vmin=vmin, vmax=vmax, aspect='equal')

    # display
    plt.show()
    plt.draw()


@plotwrapper
def hist(*args, **kwargs):
    """
    Wrapper for matplotlib.hist function

    """

    # remove kwargs that are filled in manually
    kwargs.pop('alpha', None)
    kwargs.pop('histtype', None)
    kwargs.pop('normed', None)
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

    colormap : string
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
def errorplot(x, y, ye, color='k', xscale='linear', **kwargs):
    """
    Plot a line with error bars

    """

    ax = kwargs['ax']
    ax.plot(x, y, '-', color=color)
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
