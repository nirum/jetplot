"""
PrettyPlot: Utilities for making nice and readable plots using matplotlib

"""

import matplotlib.pyplot as plt
import seaborn as sns
from functools import wraps
import numpy as np


def create_figure(f):
    """
    Function decorator for creating a new figure

    """
    @wraps(f)
    def makefig_wrapper(*args, **kwds):
        plt.figure()
        sns.set_style('white')
        return f(*args, **kwds)

    return makefig_wrapper


@create_figure
def image(img, symmetric=True, colormap='seismic'):
    """
    Visualize a matrix as an image

    Parameters
    ----------
    img : array_like
        The matrix to visualize

    symmetric : boolean, optional
        Whether or not to scale the colormap range so that it is symmetric about the image mean (Default: true).

    colormap : string, optional
        A matplotlib colormap to use (Default: 'seismic').

    """

    # image mean
    mu = np.mean(img)

    # image bounds
    img_min = np.min(img - mu)
    img_max = np.max(img - mu)
    abs_max = np.max(np.abs(img - mu))

    if symmetric:
        vmin = -abs_max
        vmax = abs_max

    else:
        vmin = img_min
        vmax = img_max

    # make the image
    plt.imshow(img, cmap=colormap, interpolation=None, vmin=vmin, vmax=vmax, aspect='equal')

    # display
    plt.show()
    plt.draw()


@create_figure
def hist2d(x, y, bins=None, range=None, cmap='hot'):
    """
    Function for visualizing a 2D histogram by binning given data

    Parameters
    ----------
    x : array_like
        The x-value of the data points to bin

    y : array_like
        The y-value of the data points to bin

    bins : array_like, optional
        Either the number of bins to use in each dimension, or the actual bin edges to use

    colormap : string
        A matplotlib colormap to use when generating the plot

    """

    # parse inputs
    if range is None:
        range = np.array([[np.min(x), np.max(x)], [np.min(y), np.max(y)]])

    if bins is None:
        bins = 25

    # compute the histogram
    counts, xedges, yedges = np.histogram2d(x, y, bins=bins, normed=True, range=range)

    # generate the plot
    plt.pcolor(xedges, yedges, counts.T, cmap=cmap)
    plt.xlim(xedges[0],xedges[-1])
    plt.ylim(yedges[0],yedges[-1])
    setfontsize()


def setfontsize(size=18):
    """
    Sets the font size of the x- and y- tick labels of the current axes

    Parameters
    ----------
    size : int
        The font size to use

    """

    ax = plt.gca()
    ax.set_xticklabels(ax.get_xticks(), fontsize=size)
    ax.set_yticklabels(ax.get_yticks(), fontsize=size)