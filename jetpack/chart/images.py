# -*- coding: utf-8 -*-
"""
Image visualization tools
"""
from functools import partial

import numpy as np
import matplotlib.pyplot as plt

from .utils import noticks, plotwrapper

__all__ = ['img', 'imv']


@plotwrapper
def img(data, mode='div', center=True, cmap=None, aspect='equal', vmin=None, vmax=None,
        cbar=False, interpolation='none', **kwargs):
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
    im = kwargs['ax'].imshow(img, cmap=cmap, interpolation=interpolation,
                             vmin=vmin, vmax=vmax, aspect=aspect)

    # colorbar
    if cbar:
        plt.colorbar(im)

    # clear ticks
    noticks(ax=kwargs['ax'])


# aliases
imv = partial(img, mode='seq')
