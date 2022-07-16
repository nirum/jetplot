"""Tests the colors module."""

from jetplot import colors
from matplotlib.axes import Axes
from matplotlib.colors import to_rgb
from matplotlib.figure import Figure


def test_palette():
    """Tests the Palette class."""
    hex_colors = ["#000000", "#444444", "#aaaaaa", "#cccccc", "#ffffff"]
    rgb_colors = list(map(to_rgb, hex_colors))
    pal = colors.Palette(rgb_colors)

    # Palette is a subclass of list.
    assert isinstance(pal, list)

    # Palette contains the right number of elements.
    assert len(pal) == 5

    # Palette hex values.
    for computed, expected in zip(pal.hex, hex_colors):
        assert computed == expected

    fig, axs = pal.plot()
    assert isinstance(fig, Figure)
    for ax in axs:
        assert isinstance(ax, Axes)


def test_rainbow():
    """Tests the rainbow function."""
    rainbow = colors.rainbow(0)
    assert isinstance(rainbow, colors.Palette)
    assert len(rainbow) == 13
    assert len(set(rainbow)) == 13
