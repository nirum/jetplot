"""Common plots."""

import numpy as np
from scipy.stats import gaussian_kde
from sklearn.covariance import EmpiricalCovariance, MinCovDet

from matplotlib.patches import Ellipse
from matplotlib.transforms import Affine2D

from .chart_utils import figwrapper, nospines, plotwrapper
from .colors import cmap_colors
from .typing import Color

__all__ = ["hist", "hist2d", "errorplot", "bar", "lines", "waterfall", "ridgeline", "circle"]


@plotwrapper
def hist(*args, **kwargs):
    """Wrapper for matplotlib.hist function."""

    # remove kwargs that are filled in manually
    kwargs.pop("alpha", None)
    kwargs.pop("histtype", None)
    kwargs.pop("normed", None)

    # get the axis and figure handles
    ax = kwargs.pop("ax")
    kwargs.pop("fig")

    return ax.hist(*args, histtype="stepfilled", alpha=0.85, normed=True, **kwargs)


@plotwrapper
def hist2d(x, y, bins=None, range=None, cmap="hot", **kwargs):
    """
    Visualizes a 2D histogram by binning data.

    Args:
      x: The x-value of the data points to bin.
      y: The y-value of the data points to bin.
      bins: Either the number of bins to use, or the actual bin edges to use.
      cmap: A matplotlib colormap to use.
    """

    # parse inputs
    if range is None:
        range = np.array([[np.min(x), np.max(x)], [np.min(y), np.max(y)]])

    if bins is None:
        bins = 25

    # compute the histogram
    cnt, xe, ye = np.histogram2d(x, y, bins=bins, normed=True, range=range)

    # generate the plot
    ax = kwargs["ax"]
    ax.pcolor(xe, ye, cnt.T, cmap=cmap)
    ax.set_xlim(xe[0], xe[-1])
    ax.set_ylim(ye[0], ye[-1])
    ax.set_aspect("equal")


@plotwrapper
def errorplot(
    x,
    y,
    yerr,
    method="patch",
    color: Color="#222222",
    xscale="linear",
    fmt="-",
    err_color: Color="#cccccc",
    alpha_fill=1.0,
    clip_on=True,
    **kwargs
):
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
        ax.fill_between(x, ymin, ymax, color=err_color, alpha=alpha_fill,
                        interpolate=True, lw=0.0, clip_on=clip_on)
        ax.plot(x, y, fmt, color=color, clip_on=clip_on)

    else:
        raise ValueError("Method must be 'line' or 'patch'")

    ax.set_xscale(xscale)


@plotwrapper
def bar(
    labels, data, color="#888888", width=0.7, err=None, capsize=5, capthick=2, **kwargs
):
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

    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    nospines(ax=ax)
    ax.tick_params(axis="x", length=0)
    ax.spines["bottom"].set_color("none")
    ax.set_xlim((0, n + width))

    return ax


@plotwrapper
def lines(x, lines=None, cmap="viridis", **kwargs):
    ax = kwargs["ax"]

    if lines is None:
        lines = list(x)
        x = np.arange(len(lines[0]))

    else:
        lines = list(lines)

    colors = cmap_colors(cmap, len(lines))
    for line, color in zip(lines, colors):
        ax.plot(x, line, color=color)


@plotwrapper
def waterfall(x, ys, dy=1.0, pad=0.1, color="#444444", ec="#cccccc", ew=2.0, **kwargs):
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
def ridgeline(t, xs, colors, edgecolor="#ffffff", ymax=0.6, **kwargs):
    fig = kwargs["fig"]
    axs = []

    for k, (x, c) in enumerate(zip(xs, colors)):
        ax = fig.add_subplot(len(xs), 1, k + 1)
        y = gaussian_kde(x).evaluate(t)
        ax.fill_between(t, y, color=c, clip_on=False)
        ax.plot(t, y, color=edgecolor, clip_on=False)
        ax.axhline(0.0, lw=2, color=c, clip_on=False)

        ax.set_xlim(t[0], t[-1])
        ax.set_xticks([])
        ax.set_xticklabels([])

        ax.set_ylim(0., ymax)
        ax.set_yticks([])
        ax.set_yticklabels([])

        nospines(ax=ax, left=True, bottom=True)
        axs.append(ax)

    return fig, axs


@plotwrapper
def circle(radius=1.0, **kwargs):
    """Plots a unit circle."""
    ax = kwargs["ax"]
    theta = np.linspace(0, 2 * np.pi, 1001)
    ax.plot(radius * np.cos(theta), radius * np.sin(theta), "-")


@plotwrapper
def ellipse(x, y, n_std=3.0, facecolor='none', estimator='empirical', **kwargs):
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
    Estimator = MinCovDet if estimator == 'robust' else EmpiricalCovariance
    cov = Estimator().fit(pts).covariance_
    
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensionl dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transform = Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transform + ax.transData)
    return ax.add_patch(ellipse)
