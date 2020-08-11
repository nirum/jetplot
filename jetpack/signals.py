"""Tools for signal processing."""

import numpy as np
from scipy.ndimage.filters import gaussian_filter1d

__all__ = ['smooth', 'canoncorr', 'participation_ratio', 'stable_rank']


def smooth(x, sigma=1.0, axis=0):
  """Smooths a 1D signal with a gaussian filter.

  Args:
    x: array_like, The array to be smoothed
    sigma: float, The width of the gaussian filter (default: 1.0)

  Returns:
  xs: array_like, A smoothed version of the input signal
  """
  return gaussian_filter1d(x, sigma, axis=axis)


def stable_rank(X):
  """Computes the stable rank of a matrix"""
  assert X.ndim == 2, "X must be a matrix"
  svals_sq = np.linalg.svd(X, compute_uv=False, full_matrices=False) ** 2
  return svals_sq.sum() / svals_sq.max()


def participation_ratio(C):
  """Computes the participation ratio of a square matrix."""
  assert C.ndim == 2, "C must be a matrix"
  assert C.shape[0] == C.shape[1], "C must be a square matrix"
  return np.trace(C) ** 2 / np.trace(np.linalg.matrix_power(C, 2))


def canoncorr(X, Y):
  """Canonical correlation between two subspaces.

  Args:
    X, Y: The subspaces to compare. They should be of the same size.

  Returns:
    corr: array_like, Cosine of the principal angles.

  Notes:
    The canonical correlation between subspaces generalizes the idea of the angle
    between vectors to linear subspaces. It is defined as recursively finding unit
    vectors in each subspace that are maximally correlated [1]_. Here, we compute
    the principal vectors and angles via the QR decomposition [2]_.

  References:
    .. [1] Angles between flats. (2016, August 4). In Wikipedia, The Free Encyclopedia.
     https://en.wikipedia.org/w/index.php?title=Angles_between_flats
    .. [2] Björck, Ȧke, and Gene H. Golub. "Numerical methods for computing angles
     between linear subspaces." Mathematics of computation 27.123 (1973): 579-594.
  """
  # Orthogonalize each subspace
  qu, qv = np.linalg.qr(X)[0], np.linalg.qr(Y)[0]

  # singular values of the inner product between the orthogonalized spaces
  return np.linalg.svd(qu.T.dot(qv), compute_uv=False, full_matrices=False)
