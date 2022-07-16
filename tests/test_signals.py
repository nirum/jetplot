"""Tests for the signals module."""

from jetplot import signals
import numpy as np


def test_stable_rank():

    U, _ = np.linalg.qr(np.random.randn(32, 32))
    V, _ = np.linalg.qr(np.random.randn(32, 32))
    S = np.random.randn(32)

    X = U @ np.diag(S) @ V.T
    expected = (S ** 2).sum() / (S ** 2).max()
    computed = signals.stable_rank(X)
    print(expected)
    print(computed)

    assert np.allclose(expected, computed)


def test_participation_ratio():

    def _random_matrix(evals):
        dim = evals.size
        Q, _ = np.linalg.qr(np.random.randn(dim, dim))
        return Q @ np.diag(evals) @ Q.T
    
    C = _random_matrix(np.array([1., 0., 0.]))
    assert np.allclose(signals.participation_ratio(C), 1.0)

    C = _random_matrix(np.array([1., 1., 1.]))
    assert np.allclose(signals.participation_ratio(C), 3.0)


def test_smooth():

    def curvature(x):
        second_derivative = np.convolve(x, [-1, 2, -1], mode='valid')
        return np.abs(second_derivative).mean()

    # Sample white noise.
    rs = np.random.RandomState(0)
    x = rs.randn(1000)

    # Smooth white noise with different sigmas.
    y1 = signals.smooth(x, sigma=1.)
    y2 = signals.smooth(x, sigma=2.)
    y3 = signals.smooth(x, sigma=5.)

    assert curvature(x) > curvature(y1) > curvature(y2) > curvature(y3)


def test_cca():
    n = 10
    k = 3
    assert k < n

    rs = np.random.RandomState(0)

    X = rs.randn(n, k)
    Y = rs.randn(n, k)
    Z = X @ np.linalg.qr(rs.randn(k, k))[0]

    # Correlation with itself should be all ones.
    xx = signals.canoncorr(X, X)
    assert np.allclose(xx, np.ones(k))

    # Correlation with a different random subspace.
    xy = signals.canoncorr(X, Y)
    assert np.all(xy <= 1.)
    assert np.all(0. <= xy)
    assert 0 < np.sum(xy) < k

    # Correlation with random rotation should be all ones.
    xz = signals.canoncorr(X, Z)
    assert np.allclose(xz, np.ones(k))

def test_normalize():

    X = np.random.randn(10, 3)
    expected = np.stack([x / np.linalg.norm(x) for x in X])
    computed = signals.normalize(X)
    assert np.allclose(expected, computed)

    X = np.random.rand(4, 6)
    expected = np.stack([x / np.linalg.norm(x) for x in X.T]).T
    computed = signals.normalize(X, axis=0)
    assert np.allclose(expected, computed)
