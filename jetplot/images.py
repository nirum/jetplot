"""Image visualization tools."""

from functools import partial

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import FixedLocator

from . import colors as c
from .chart_utils import noticks, plotwrapper

__all__ = ["img", "imv", "fsurface", "cmat"]


@plotwrapper
def img(
    data,
    mode="div",
    cmap=None,
    aspect="equal",
    vmin=None,
    vmax=None,
    cbar=True,
    interpolation="none",
    **kwargs,
):
    """Visualize a matrix as an image.

    Args:
      img: array_like, The array to visualize.
      mode: string, Either 'div' for a diverging image or 'seq' for
        sequential (default: 'div').
      cmap: string, Colormap to use.
      aspect: string, Either 'equal' or 'auto'
    """
    # work with a copy of the original image data
    img = np.squeeze(data.copy())

    # image bounds
    img_min = np.min(img)
    img_max = np.max(img)
    abs_max = np.max(np.abs(img))

    if mode == "div":
        if vmin is None:
            vmin = -abs_max
        if vmax is None:
            vmax = abs_max
        if cmap is None:
            cmap = "seismic"
    elif mode == "seq":
        if vmin is None:
            vmin = img_min
        if vmax is None:
            vmax = img_max
        if cmap is None:
            cmap = "viridis"
    elif mode == "cov":
        vmin, vmax, cmap, cbar = 0, 1, "viridis", True
    elif mode == "cov":
        vmin, vmax, cmap, cbar = -1, 1, "seismic", True
    else:
        raise ValueError("Unrecognized mode: '" + mode + "'")

    # make the image
    im = kwargs["ax"].imshow(
        img, cmap=cmap, interpolation=interpolation, vmin=vmin, vmax=vmax, aspect=aspect
    )

    # colorbar
    if cbar:
        plt.colorbar(im)

    # clear ticks
    noticks(ax=kwargs["ax"])

    return im


@plotwrapper
def fsurface(func, xrng=None, yrng=None, n=100, nargs=2, **kwargs):
    xrng = (-1, 1) if xrng is None else xrng
    yrng = xrng if yrng is None else yrng

    xs = np.linspace(*xrng, n)
    ys = np.linspace(*yrng, n)

    xm, ym = np.meshgrid(xs, ys)

    if nargs == 1:
        zz = np.vstack((xm.ravel(), ym.ravel()))
        args = (zz,)
    elif nargs == 2:
        args = (xm.ravel(), ym.ravel())
    else:
        raise ValueError(f"Invalid value for nargs ({nargs})")

    zm = func(*args).reshape(xm.shape)

    kwargs["ax"].contourf(xm, ym, zm)


@plotwrapper
def cmat(
    arr,
    labels=None,
    annot=True,
    cmap="gist_heat_r",
    cbar=False,
    fmt="0.0%",
    dark_color="#222222",
    light_color="#dddddd",
    grid_color=c.gray[9],
    theta=0.5,
    label_fontsize=10.0,
    fontsize=10.0,
    vmin=0.0,
    vmax=1.0,
    **kwargs,
):
    """Plot confusion matrix."""
    num_rows, num_cols = arr.shape

    ax = kwargs.pop("ax")
    cb = imv(arr, ax=ax, vmin=vmin, vmax=vmax, cmap=cmap, cbar=cbar)

    xs, ys = np.meshgrid(np.arange(num_cols), np.arange(num_rows))
    for x, y, value in zip(xs.flat, ys.flat, arr.flat):
        color = dark_color if (value <= theta) else light_color
        annot = f"{{:{fmt}}}".format(value)
        ax.text(x, y, annot, ha="center", va="center", color=color, fontsize=fontsize)

    if labels is not None:
        ax.set_xticks(np.arange(num_cols))
        ax.set_xticklabels(labels, rotation=90, fontsize=label_fontsize)
        ax.set_yticks(np.arange(num_rows))
        ax.set_yticklabels(labels, label_fontsize=label_fontsize)

    ax.xaxis.set_minor_locator(FixedLocator(np.arange(num_cols) - 0.5))
    ax.yaxis.set_minor_locator(FixedLocator(np.arange(num_rows) - 0.5))

    ax.grid(
        visible=True,
        which="minor",
        axis="both",
        linewidth=1.0,
        color=grid_color,
        linestyle="-",
        alpha=1.0,
    )

    return cb, ax


# aliases
imv = partial(img, mode="seq")
