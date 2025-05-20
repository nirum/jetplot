import numpy as np
from matplotlib import pyplot as plt

from jetplot import plots


def test_hist():
    bins = 11
    x = np.arange(10)
    fig, ax = plt.subplots()
    values, bin_edges, patches = plots.hist(x, bins=bins, fig=fig, ax=ax)
    assert len(values) == bins
    assert len(bin_edges) == bins + 1
    plt.close(fig)


def test_hist2d():
    x = np.random.randn(100)
    y = np.random.randn(100)
    fig, ax = plt.subplots()
    plots.hist2d(x, y, fig=fig, ax=ax)
    assert ax.get_aspect() == 1.0
    plt.close(fig)


def test_errorplot_methods():
    x = np.arange(5)
    y = np.arange(5)
    yerr = np.ones_like(x)

    fig, ax = plt.subplots()
    plots.errorplot(x, y, yerr, method="patch", fig=fig, ax=ax)
    assert len(ax.lines) == 1
    plt.close(fig)

    fig, ax = plt.subplots()
    plots.errorplot(x, y, yerr, method="line", fig=fig, ax=ax)
    assert len(ax.lines) > 1
    plt.close(fig)


def test_circle():
    fig, ax = plt.subplots()
    plots.circle(fig=fig, ax=ax)
    line = ax.lines[0]
    assert line.get_xdata()[0] == 1.0
    assert len(line.get_xdata()) == 1001
    plt.close(fig)


def test_bar_and_lines():
    labels = ["A", "B", "C"]
    data = [1.0, 2.0, 3.0]
    err = [0.1, 0.1, 0.1]

    fig, ax = plt.subplots()
    plots.bar(labels, data, err=err, fig=fig, ax=ax)
    assert len(ax.patches) >= len(labels)
    plt.close(fig)

    fig, ax = plt.subplots()
    lines = [np.array(data), np.array(data) + 1]
    plots.lines(np.arange(3), lines=lines, fig=fig, ax=ax)
    assert len(ax.lines) == len(lines)
    plt.close(fig)


def test_waterfall():
    x = np.arange(5)
    ys = [np.linspace(0, 1, 5) for _ in range(3)]
    fig, ax = plt.subplots()
    plots.waterfall(x, ys, fig=fig, ax=ax)
    # waterfall uses fill_between which adds PolyCollections
    assert len(ax.collections) >= len(ys)
    plt.close(fig)


def test_violinplot():
    data = np.random.randn(100)
    fig, ax = plt.subplots()
    plots.violinplot(data, xs=1, fig=fig, ax=ax)
    # Expect at least one polygon from violin body
    assert len(ax.collections) > 0
    plt.close(fig)
