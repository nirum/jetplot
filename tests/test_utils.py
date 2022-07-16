"""Tests chart utilities."""

from itertools import product
from jetplot import chart_utils as cu
from matplotlib import pyplot as plt


def test_wrappers():
    
    @cu.figwrapper
    def fig_func(**kwargs):
        assert 'fig' in kwargs

    def ax_func(**kwargs):
        assert 'fig' in kwargs
        assert 'ax' in kwargs

    fig_func()
    cu.axwrapper(ax_func)()
    cu.plotwrapper(ax_func)()


def test_noticks():
    """Tests all combinations of removing spines."""

    compass = ('left', 'right', 'top', 'bottom')
    args = ((True, False),) * len(compass)

    for bools in product(*args):
        kwargs = dict(zip(compass, bools))

        fig, ax = plt.subplots()
        ax.plot([1, 2, 3, 4, 5])
        cu.nospines(ax=ax, **kwargs)

        for key, spine in ax.spines.items():
            assert spine.get_visible() == (not kwargs[key])

        plt.close(fig)
