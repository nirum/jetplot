"""Common plots."""

from collections.abc import Iterable, Sequence
from typing import Any

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Ellipse
from matplotlib.transforms import Affine2D
from matplotlib.typing import ColorType
from numpy.typing import NDArray
from scipy.stats import gaussian_kde
from sklearn.covariance import EmpiricalCovariance, MinCovDet

from .chart_utils import figwrapper, nospines, plotwrapper
from .colors import cmap_colors, neutral

__all__ = [
    "hist",
    "hist2d",
    "errorplot",
    "violinplot",
    "bar",
    "lines",
    "waterfall",
    "ridgeline",
    "circle",
]


@plotwrapper
def violinplot(
    data: NDArray[np.floating],
    xs: Sequence[float] | float,
    fc: ColorType = neutral[3],
    ec: ColorType = neutral[9],
    mc: ColorType = neutral[1],
    showmedians: bool = True,
    showmeans: bool = False,
    showquartiles: bool = True,
    **kwargs: Any,
) -> Axes:
    """Violin plot with customizable elements."""
    _ = kwargs.pop("fig")
    ax = kwargs.pop("ax")

    data = np.atleast_2d(data).T

    if isinstance(xs, float) or isinstance(xs, int):
        xs = [
            xs,
        ]

    parts = ax.violinplot(
        data, positions=xs, showmeans=False, showmedians=False, showextrema=False
    )

    for pc in parts["bodies"]:
        pc.set_facecolor(fc)
        pc.set_edgecolor(ec)
        pc.set_alpha(1.0)

    # pyrefly: ignore  # no-matching-overload, bad-argument-type
    q1, medians, q3 = np.percentile(data, [25, 50, 75], axis=0)

    ax.vlines(
        xs,
        np.min(data, axis=0),
        np.max(data, axis=0),
        color=ec,
        linestyle="-",
        lw=1,
        zorder=10,
        label="Extrema",
    )

    if showquartiles:
        ax.vlines(xs, q1, q3, color=ec, linestyle="-", lw=5, zorder=5)

    if showmedians:
        ax.scatter(xs, medians, marker="o", color=mc, s=15, zorder=20)

    if showmeans:
        ax.scatter(
            xs,
            # pyrefly: ignore  # no-matching-overload, bad-argument-type
            np.mean(data, axis=0),
            marker="s",
            color=mc,
            s=15,
            zorder=20,
        )

    return ax


@plotwrapper
def hist(
    *args: Any, histtype="stepfilled", alpha=0.85, density=True, **kwargs: Any
) -> Any:
    """Wrapper for matplotlib.hist function."""
    ax = kwargs.pop("ax")
    kwargs.pop("fig")

    return ax.hist(*args, histtype=histtype, alpha=alpha, density=density, **kwargs)


@plotwrapper
def hist2d(
    x: NDArray[np.floating],
    y: NDArray[np.floating],
    bins: int | Sequence[float] | None = None,
    limits: NDArray[np.floating] | Sequence[Sequence[float]] | None = None,
    cmap: str = "hot",
    **kwargs: Any,
) -> None:
    """
    Visualizes a 2D histogram by binning data.

    Args:
      x: The x-value of the data points to bin.
      y: The y-value of the data points to bin.
      bins: Either the number of bins to use, or the actual bin edges to use.
      cmap: A matplotlib colormap to use.
    """

    # parse inputs
    if limits is None:
        limits = np.array([[np.min(x), np.max(x)], [np.min(y), np.max(y)]])

    if bins is None:
        bins = 25

    # compute the histogram
    # pyrefly: ignore  # no-matching-overload, bad-argument-type
    cnt, xe, ye = np.histogram2d(x, y, bins=bins, range=limits, density=True)

    # generate the plot
    ax = kwargs["ax"]
    ax.pcolor(xe, ye, cnt.T, cmap=cmap)
    ax.set_xlim(xe[0], xe[-1])
    ax.set_ylim(ye[0], ye[-1])
    ax.set_aspect("equal")


@plotwrapper
def errorplot(
    x: NDArray[np.floating],
    y: NDArray[np.floating],
    yerr: NDArray[np.floating]
    | float
    | tuple[NDArray[np.floating], NDArray[np.floating]],
    method: str = "patch",
    color: ColorType = "#222222",
    xscale: str = "linear",
    fmt: str = "-",
    err_color: ColorType = "#cccccc",
    alpha_fill: float = 1.0,
    clip_on: bool = True,
    **kwargs: Any,
) -> None:
    """Plot a line with error bars."""
    ax = kwargs["ax"]

    if np.isscalar(yerr) or len(yerr) == len(y):
        ymin = y - yerr
        ymax = y + yerr
    elif len(yerr) == 2:
        ymin, ymax = yerr
    else:
        raise ValueError("Invalid yerr value: ", yerr)

    if method == "line":
        ax.plot(x, y, fmt, color=color, linewidth=4, clip_on=clip_on)
        ax.plot(x, ymax, "_", ms=20, color=err_color, clip_on=clip_on)
        ax.plot(x, ymin, "_", ms=20, color=err_color, clip_on=clip_on)
        for i, xi in enumerate(x):
            ax.plot(
                np.array([xi, xi]),
                np.array([ymin[i], ymax[i]]),
                "-",
                color=err_color,
                linewidth=2,
                clip_on=clip_on,
            )

    elif method == "patch":
        ax.fill_between(
            x,
            ymin,
            ymax,
            color=err_color,
            alpha=alpha_fill,
            interpolate=True,
            lw=0.0,
            clip_on=clip_on,
        )
        ax.plot(x, y, fmt, color=color, clip_on=clip_on)

    else:
        raise ValueError("Method must be 'line' or 'patch'")

    ax.set_xscale(xscale)


@plotwrapper
def bar(
    labels: Sequence[str],
    data: Sequence[float],
    color: ColorType = "#888888",
    width: float = 0.7,
    offset: float = 0.0,
    err: Sequence[float] | None = None,
    capsize: float = 5,
    capthick: float = 2,
    **kwargs: Any,
) -> Axes:
    """Bar chart.

    Args:
      labels: list or iterable of text labels
      data: list or iterable of numerical values to plot
      color: color of the bars (default: #888888)
      width: width of the bars (default: 0.7)
      err: list or iterable of error bar values (default: None)
    """
    ax = kwargs["ax"]

    n = len(data)
    x = np.arange(n) + width
    if err is not None:
        err = np.vstack((np.zeros_like(err), err))

    ax.bar(x, data, width, color=color)

    if err is not None:
        caplines = ax.errorbar(
            x,
            data,
            err,
            capsize=capsize,
            capthick=capthick,
            fmt="none",
            marker=None,
            color=color,
        )[1]
        caplines[0].set_markeredgewidth(0)

    ax.set_xticks(x - offset)
    ax.set_xticklabels(labels)

    nospines(ax=ax)
    ax.tick_params(axis="x", length=0)
    ax.spines["bottom"].set_color("none")
    ax.set_xlim((0 - offset, n + width + offset))

    return ax


@plotwrapper
def lines(
    x: NDArray[np.floating] | NDArray[np.integer],
    lines: list[NDArray[np.floating]] | None = None,
    cmap: str = "viridis",
    **kwargs,
) -> Axes:
    """Plot multiple lines using a color map."""
    ax = kwargs["ax"]

    if lines is None:
        lines = list(x)  # pyrefly: ignore
        x = np.arange(len(lines[0]))

    else:
        lines = list(lines)

    colors = cmap_colors(cmap, len(lines))
    for line, color in zip(lines, colors, strict=False):
        ax.plot(x, line, color=color)

    return ax


@plotwrapper
def waterfall(
    x: NDArray[np.floating],
    ys: Iterable[NDArray[np.floating]],
    dy: float = 1.0,
    pad: float = 0.1,
    color: ColorType = "#444444",
    ec: ColorType = "#cccccc",
    ew: float = 2.0,
    **kwargs: Any,
) -> None:
    """Waterfall plot."""
    ax = kwargs["ax"]
    total = len(ys)

    for index, y in enumerate(ys):
        zorder = total - index
        y = y * dy + index
        ax.plot(x, y + pad, color=ec, clip_on=False, lw=ew, zorder=zorder)
        ax.fill_between(x, y, index, color=color, zorder=zorder, clip_on=False)

    ax.set_ylim(0, total)
    ax.set_xlim(x[0], x[-1])


@figwrapper
def ridgeline(
    t: NDArray[np.floating],
    xs: Iterable[NDArray[np.floating]],
    colors: Iterable[ColorType],
    edgecolor: ColorType = "#ffffff",
    ymax: float = 0.6,
    **kwargs: Any,
) -> tuple[Figure, list[Axes]]:
    """Stacked density plots reminiscent of a ridgeline plot."""
    fig = kwargs["fig"]
    axs = []

    for k, (x, c) in enumerate(zip(xs, colors, strict=False)):
        ax = fig.add_subplot(len(xs), 1, k + 1)
        y = gaussian_kde(x).evaluate(t)
        ax.fill_between(t, y, color=c, clip_on=False)
        ax.plot(t, y, color=edgecolor, clip_on=False)
        ax.axhline(0.0, lw=2, color=c, clip_on=False)

        ax.set_xlim(t[0], t[-1])
        ax.set_xticks([])
        ax.set_xticklabels([])

        ax.set_ylim(0.0, ymax)
        ax.set_yticks([])
        ax.set_yticklabels([])

        nospines(ax=ax, left=True, bottom=True)
        axs.append(ax)

    return fig, axs


@plotwrapper
def circle(radius: float = 1.0, **kwargs: Any) -> None:
    """Plots a unit circle."""
    ax = kwargs["ax"]
    theta = np.linspace(0, 2 * np.pi, 1001)
    ax.plot(radius * np.cos(theta), radius * np.sin(theta), "-")


@plotwrapper
def ellipse(
    x: NDArray[np.floating],
    y: NDArray[np.floating],
    n_std: float = 3.0,
    facecolor: str = "none",
    estimator: str = "empirical",
    **kwargs: Any,
) -> Ellipse:
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    **kwargs
        Forwarded to `~matplotlib.patches.Ellipse`

    Returns
    -------
    matplotlib.patches.Ellipse
    """
    ax = kwargs.get("ax")

    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    # cov = np.cov(x, y)
    pts = np.vstack((x, y)).T
    Estimator = MinCovDet if estimator == "robust" else EmpiricalCovariance
    cov = Estimator().fit(pts).covariance_

    pearson = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensional dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse(
        (0, 0),
        width=ell_radius_x * 2,
        height=ell_radius_y * 2,
        facecolor=facecolor,
        **kwargs,
    )

    # Calculating the standard deviation of x from
    # the square root of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the standard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transform = (
        Affine2D()
        .rotate_deg(45)
        .scale(float(scale_x), float(scale_y))
        .translate(float(mean_x), float(mean_y))
    )

    ellipse.set_transform(transform + ax.transData)
    return ax.add_patch(ellipse)
