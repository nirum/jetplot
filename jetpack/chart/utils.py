# -*- coding: utf-8 -*-
"""
Utils
"""
from __future__ import (absolute_import, division, print_function, unicode_literals)
import matplotlib.pyplot as plt
from functools import wraps

__all__ = ['setfontsize', 'noticks', 'nospines', 'breathe', 'setcolor', 'tickdir']


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

    return ax


@axwrapper
def noticks(**kwargs):
    """
    Clears tick marks (useful for images)
    """

    ax = kwargs['ax']
    ax.set_xticks([])
    ax.set_yticks([])


@axwrapper
def nospines(left=False, bottom=False, top=True, right=True, **kwargs):
    """
    Hides the specified axis spines (by default, right and top spines)
    """

    ax = kwargs['ax']

    # assemble args into dict
    disabled = dict(left=left, right=right, top=top, bottom=bottom)

    # disable spines
    for key in disabled:
        if disabled[key]:
            ax.spines[key].set_color('none')

    # disable xticks
    if disabled['top'] and disabled['bottom']:
        ax.set_xticks([])
    elif disabled['top']:
        ax.xaxis.set_ticks_position('bottom')
    elif disabled['bottom']:
        ax.xaxis.set_ticks_position('top')

    # disable yticks
    if disabled['left'] and disabled['right']:
        ax.set_yticks([])
    elif disabled['left']:
        ax.yaxis.set_ticks_position('right')
    elif disabled['right']:
        ax.yaxis.set_ticks_position('left')

    return ax


@axwrapper
def breathe(factor=0.05, direction='out', **kwargs):
    """
    Adds space between axes and plot
    """
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
    tickdir(direction=direction, **kwargs)

    return ax


@axwrapper
def tickdir(direction, **kwargs):
    ax = kwargs['ax']

    ax.xaxis.set_tick_params(direction=direction)
    ax.yaxis.set_tick_params(direction=direction)

    return ax


@axwrapper
def setcolor(color='#444444', **kwargs):
    ax = kwargs['ax']

    # set the tick parameters
    ax.tick_params(axis='x', colors=color)
    ax.tick_params(axis='y', colors=color)

    # set the label colors
    ax.xaxis.label.set_color(color)
    ax.yaxis.label.set_color(color)
    ax.set_xlabel(ax.get_xlabel(), color=color)
    ax.set_ylabel(ax.get_ylabel(), color=color)

    return ax
