"""Tests for the timepiece module."""

import time

import numpy as np

from jetplot.timepiece import hrtime, profile


def test_hrtime():
    # test numeric input
    assert hrtime(1e6) == "1 weeks, 4 days, 13 hours, 46 min., 40 s"
    assert hrtime(2e5) == "2 days, 7 hours, 33 min., 20 s"
    assert hrtime(5e3) == "1 hours, 23 min., 20 s"
    assert hrtime(60) == "1 min., 0 s"
    assert hrtime(1) == "1 s"
    assert hrtime(0) == "0 s"
    assert hrtime(0.1) == "100 ms"
    assert hrtime(0.005) == "5 ms"
    assert hrtime(1e-5) == "10 {}s".format("\u03bc")
    assert hrtime(5.25e-4) == "525 {}s".format("\u03bc")
    assert hrtime(5e-7) == "500 ns"
    assert hrtime(1e-12) == "0.001 ns"


def test_profile():
    T = 0.2
    K = 3

    wrapper = profile(time.sleep)
    for _ in range(K):
        wrapper(T)

    # pyrefly: ignore  # missing-attribute
    assert isinstance(wrapper.calls, list)
    assert len(wrapper.calls) == K
    # pyrefly: ignore  # missing-attribute
    assert np.allclose(wrapper.mean(), T, atol=0.01)
    # pyrefly: ignore  # missing-attribute
    assert np.allclose(wrapper.serr(), 0.0, atol=0.01)
    # pyrefly: ignore  # missing-attribute
    assert wrapper.summary() is None
