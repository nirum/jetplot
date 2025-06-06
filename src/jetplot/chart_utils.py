"""Plotting utils."""

from collections.abc import Callable
from functools import partial, wraps
from typing import Any, Literal

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes

__all__ = [
    "noticks",
    "nospines",
    "breathe",
    "plotwrapper",
    "figwrapper",
    "axwrapper",
    "get_bounds",
    "yclamp",
    "xclamp",
]


def figwrapper(fun: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that adds figure handles to the kwargs of a function."""

    @wraps(fun)
    def wrapper(*args, **kwargs):
        if "fig" not in kwargs:
            figsize = kwargs.get("figsize", None)
            kwargs["fig"] = plt.figure(figsize=figsize)
        return fun(*args, **kwargs)

    return wrapper


def plotwrapper(fun: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that adds figure and axes handles to the kwargs of a function."""

    @wraps(fun)
    def wrapper(*args, **kwargs):
        if "ax" not in kwargs:
            if "fig" not in kwargs:
                figsize = kwargs.get("figsize", None)
                kwargs["fig"] = plt.figure(figsize=figsize)
            kwargs["ax"] = kwargs["fig"].add_subplot(111)
        else:
            if "fig" not in kwargs:
                kwargs["fig"] = kwargs["ax"].get_figure()

        return fun(*args, **kwargs)

    return wrapper


def axwrapper(fun: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that adds an axes handle to kwargs."""

    @wraps(fun)
    def wrapper(*args, **kwargs):
        if "ax" not in kwargs:
            if "fig" not in kwargs:
                kwargs["fig"] = plt.gcf()
            kwargs["ax"] = plt.gca()
        else:
            if "fig" not in kwargs:
                kwargs["fig"] = kwargs["ax"].get_figure()
        return fun(*args, **kwargs)

    return wrapper


@axwrapper
def noticks(**kwargs: Any) -> None:
    """
    Clears tick marks (useful for images)
    """

    ax = kwargs["ax"]
    ax.set_xticks([])
    ax.set_yticks([])


@axwrapper
def nospines(
    left: bool = False,
    bottom: bool = False,
    top: bool = True,
    right: bool = True,
    **kwargs: Any,
) -> plt.Axes:
    """
    Hides the specified axis spines (by default, right and top spines)
    """

    ax = kwargs["ax"]

    # assemble args into dict
    disabled = dict(left=left, right=right, top=top, bottom=bottom)

    # disable spines
    for key in disabled:
        if disabled[key]:
            ax.spines[key].set_visible(False)

    # disable xticks
    if disabled["top"] and disabled["bottom"]:
        ax.set_xticks([])
    elif disabled["top"]:
        ax.xaxis.set_ticks_position("bottom")
    elif disabled["bottom"]:
        ax.xaxis.set_ticks_position("top")

    # disable yticks
    if disabled["left"] and disabled["right"]:
        ax.set_yticks([])
    elif disabled["left"]:
        ax.yaxis.set_ticks_position("right")
    elif disabled["right"]:
        ax.yaxis.set_ticks_position("left")

    return ax


def get_bounds(axis: Literal["x", "y"], ax: Axes | None = None) -> tuple[float, float]:
    """Return the axis spine bounds for the given axis.

    Parameters
    ----------
    axis : str
        Axis to inspect, either ``"x"`` or ``"y"``.
    ax : matplotlib.axes.Axes | None, optional
        Axes object to inspect. If ``None``, the current axes are used.

    Returns
    -------
    tuple[float, float]
        Lower and upper bounds of the axis spine.
    """
    if ax is None:
        ax = plt.gca()

    axis_map: dict[str, Any] = {
        "x": (ax.get_xticks, ax.get_xticklabels, ax.get_xlim, "bottom"),
        "y": (ax.get_yticks, ax.get_yticklabels, ax.get_ylim, "left"),
    }

    # get functions
    ticks, labels, limits, spine_key = axis_map[axis]

    if ax.spines[spine_key].get_bounds():
        return ax.spines[spine_key].get_bounds()
    else:
        lower, upper = None, None

        for tick, label in zip(list(ticks()), list(labels()), strict=True):
            if label.get_text() != "":
                if lower is None:
                    lower = tick
                else:
                    upper = tick

        if lower is None or upper is None:
            return limits()

    return lower, upper


@axwrapper
def breathe(
    xlims: tuple[float, float] | None = None,
    ylims: tuple[float, float] | None = None,
    padding_percent: float = 0.05,
    **kwargs: Any,
) -> plt.Axes:
    """Adds space between axes and plot."""
    ax = kwargs["ax"]

    def identity(x):
        return x

    if ax.get_xscale() == "log":
        xfwd = np.log10
        xrev = partial(np.power, 10)
    else:
        xfwd = identity
        xrev = identity

    if ax.get_yscale() == "log":
        yfwd = np.log10
        yrev = partial(np.power, 10)
    else:
        yfwd = identity
        yrev = identity

    xmin, xmax = xfwd(ax.get_xlim()) if xlims is None else xlims
    ymin, ymax = yfwd(ax.get_ylim()) if ylims is None else ylims

    xdelta = (xmax - xmin) * padding_percent
    ydelta = (ymax - ymin) * padding_percent

    ax.set_xlim(xrev(xmin - xdelta), xrev(xmax + xdelta))
    ax.spines["bottom"].set_bounds(xrev(xmin), xrev(xmax))

    ax.set_ylim(yrev(ymin - ydelta), yrev(ymax + ydelta))
    ax.spines["left"].set_bounds(yrev(ymin), yrev(ymax))

    nospines(**kwargs)

    return ax


@axwrapper
def yclamp(
    y0: float | None = None,
    y1: float | None = None,
    dt: float | None = None,
    **kwargs: Any,
) -> Axes:
    """Clamp the y-axis to evenly spaced tick marks."""
    ax = kwargs["ax"]

    lims = ax.get_ylim()
    y0 = lims[0] if y0 is None else y0
    y1 = lims[1] if y1 is None else y1

    ticks: list[float] = ax.get_yticks()  # pyrefly: ignore
    dt = float(np.mean(np.diff(ticks))) if dt is None else float(dt)

    new_ticks = np.arange(dt * np.floor(y0 / dt), dt * (np.ceil(y1 / dt) + 1), dt)
    ax.set_yticks(new_ticks)
    ax.set_yticklabels(new_ticks)
    ax.set_ylim(new_ticks[0], new_ticks[-1])

    return ax


@axwrapper
def xclamp(
    x0: float | None = None,
    x1: float | None = None,
    dt: float | None = None,
    **kwargs: Any,
) -> Axes:
    """Clamp the x-axis to evenly spaced tick marks."""
    ax = kwargs["ax"]

    lims = ax.get_xlim()
    x0 = lims[0] if x0 is None else x0
    x1 = lims[1] if x1 is None else x1

    ticks: list[float] = ax.get_xticks()  # pyrefly: ignore
    dt = float(np.mean(np.diff(ticks))) if dt is None else float(dt)

    new_ticks = np.arange(dt * np.floor(x0 / dt), dt * (np.ceil(x1 / dt) + 1), dt)
    ax.set_xticks(new_ticks)
    ax.set_xticklabels(new_ticks)
    ax.set_xlim(new_ticks[0], new_ticks[-1])

    return ax
