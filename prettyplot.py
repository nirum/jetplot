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

def closeall():
    """
    Close all open figure windows

    """
    plt.close('all')