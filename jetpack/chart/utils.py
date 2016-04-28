"""
Utils
"""
from __future__ import (absolute_import, division, print_function, unicode_literals)
import matplotlib.pyplot as plt
from functools import wraps

__all__ = ['setfontsize', 'noticks', 'nospines', 'breathe']


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

        fun(*args, **kwargs)
        plt.show()
        plt.draw()
        return kwargs['ax']

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
        fun(*args, **kwargs)
        plt.show()
        plt.draw()
        return kwargs['ax']

    return wrapper


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
