"""
Tests for the signals module

"""

from jetpack import signals
import numpy as np
import pytest


def test_arr():

    assert np.allclose(signals.arr(range(5)), np.arange(5))
    assert np.allclose(signals.arr(map(lambda x: x**2, [1, 4, 10])),
                       np.array([1, 16, 100]))
    assert np.all(signals.arr('abc') == np.array(list('abc')))


def test_sq():

    assert signals.sq(np.random.randn(9)).shape == (3,3)
    assert np.allclose(signals.sq(np.arange(4)), np.array([[0,1],[2,3]]))
    assert signals.sq(np.random.rand(2,2,4)).shape == (4,4)

    with pytest.raises(ValueError) as context:
        signals.sq(np.random.randn(12))

    assert 'Error: the input size is inconsistent with a square' in \
        str(context.value)


def test_sfthr():

    x = np.linspace(-2, 2, 5)
    assert np.allclose(signals.sfthr(x, 0.5),
                       np.array([-1.5, -0.5, 0, 0.5, 1.5]))
    assert np.allclose(signals.sfthr(x, 1.5),
                       np.array([-0.5, 0, 0, 0, 0.5]))

    assert np.all(signals.sfthr(np.random.rand(10), 2) == 0)
