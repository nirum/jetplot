"""Tests chart utilities."""

from itertools import product

from matplotlib import pyplot as plt

from jetplot import chart_utils as cu


def test_wrappers():
    @cu.figwrapper
    def fig_func(**kwargs):
        assert "fig" in kwargs

    def ax_func(**kwargs):
        assert "fig" in kwargs
        assert "ax" in kwargs

    fig_func()
    cu.axwrapper(ax_func)()
    cu.plotwrapper(ax_func)()


def test_nospines():
    """Tests all combinations of removing spines."""

    compass = ("left", "right", "top", "bottom")
    args = ((True, False),) * len(compass)

    for bools in product(*args):
        kwargs = dict(zip(compass, bools, strict=False))

        fig, ax = plt.subplots()
        ax.plot([1, 2, 3, 4, 5])
        cu.nospines(ax=ax, **kwargs)

        for key, spine in ax.spines.items():
            assert spine.get_visible() == (not kwargs[key])

        plt.close(fig)


def test_noticks():
    """Tests that noticks removes both x and y ticks."""

    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4, 5])
    cu.noticks(ax=ax)

    assert len(ax.get_xticks()) == 0
    assert len(ax.get_yticks()) == 0

    plt.close(fig)


def test_get_bounds_spines():
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    ax.spines["bottom"].set_bounds(0, 1)
    ax.spines["left"].set_bounds(-1, 2)

    assert cu.get_bounds("x", ax=ax) == (0, 1)
    assert cu.get_bounds("y", ax=ax) == (-1, 2)
    plt.close(fig)


def test_get_bounds_label_fallback():
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2, 3], [0, 1, 2, 3])
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(["", "a", "", "b"])

    assert cu.get_bounds("x", ax=ax) == (1, 3)
    plt.close(fig)


def test_breathe_adds_padding_and_hides_spines():
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    old_xlim = ax.get_xlim()
    old_ylim = ax.get_ylim()

    cu.breathe(ax=ax)

    new_xlim = ax.get_xlim()
    new_ylim = ax.get_ylim()

    assert new_xlim[0] < old_xlim[0] and new_xlim[1] > old_xlim[1]
    assert new_ylim[0] < old_ylim[0] and new_ylim[1] > old_ylim[1]

    assert not ax.spines["top"].get_visible()
    assert not ax.spines["right"].get_visible()
    assert ax.spines["bottom"].get_bounds() == old_xlim
    assert ax.spines["left"].get_bounds() == old_ylim
    plt.close(fig)


def test_xclamp_yclamp():
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])

    cu.xclamp(x0=0.5, x1=3.4, dt=1.0, ax=ax)
    assert ax.get_xlim() == (0.0, 4.0)
    assert list(ax.get_xticks()) == [0.0, 1.0, 2.0, 3.0, 4.0]

    cu.yclamp(y0=0.2, y1=3.5, dt=1.0, ax=ax)
    assert ax.get_ylim() == (0.0, 4.0)
    assert list(ax.get_yticks()) == [0.0, 1.0, 2.0, 3.0, 4.0]
    plt.close(fig)
