"""Tests demo functions."""

from jetplot import demo


def test_peaks():
    """Smoke test for the peaks function."""
    n = 256
    xm, ym, zm = demo.peaks(n=n)

    assert xm.shape == ym.shape == zm.shape == (n, n)
