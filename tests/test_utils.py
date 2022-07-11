"""Tests chart utilities."""

from jetplot import chart_utils as cu


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
