"""Tools for signal processing."""

from __future__ import annotations

from typing import Any, Protocol, SupportsIndex

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.ndimage import gaussian_filter1d

__all__ = ["smooth", "canoncorr", "participation_ratio", "stable_rank", "normalize"]

FloatArray = NDArray[np.floating]


def smooth(x: ArrayLike, sigma: float = 1.0, axis: int = 0) -> NDArray[np.floating]:
    """Smooths a 1D signal with a gaussian filter.

    Args:
      x: array_like, The array to be smoothed
      sigma: float, The width of the gaussian filter (default: 1.0)

    Returns:
    xs: array_like, A smoothed version of the input signal
    """
    arr = np.asarray(x)
    return gaussian_filter1d(arr, sigma, axis=axis)


def stable_rank(X: NDArray[np.floating[Any]]) -> float:
    """Compute the stable rank of a matrix.

    Args:
        X: Two-dimensional array representing a matrix.

    Raises:
        ValueError: If ``X`` is not two-dimensional.
    """
    if X.ndim != 2:
        raise ValueError("X must be a matrix")

    # pyrefly: ignore
    svals_sq = np.linalg.svd(X, compute_uv=False, full_matrices=False) ** 2

    return svals_sq.sum() / svals_sq.max()


def participation_ratio(C: np.ndarray) -> float:
    """Compute the participation ratio of a square matrix."""

    if C.ndim != 2:
        raise ValueError("C must be a matrix")

    if C.shape[0] != C.shape[1]:
        raise ValueError("C must be a square matrix")

    diag_sum = float(np.trace(C))
    diag_sq_sum = float(np.trace(C @ C))
    return diag_sum**2 / diag_sq_sum


def canoncorr(X: FloatArray, Y: FloatArray) -> FloatArray:
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
      .. [1] Angles between flats. (2016, August 4). In Wikipedia, The Free Encyclopedia
       https://en.wikipedia.org/w/index.php?title=Angles_between_flats
      .. [2] Björck, Ȧke, and Gene H. Golub. "Numerical methods for computing angles
       between linear subspaces." Mathematics of computation 27.123 (1973): 579-594.
    """
    # Orthogonalize each subspace
    # pyrefly: ignore  # no-matching-overload, bad-argument-type
    Qx, _ = np.linalg.qr(X, mode="reduced")
    # pyrefly: ignore  # no-matching-overload, bad-argument-type
    Qy, _ = np.linalg.qr(Y, mode="reduced")

    # singular values of the inner product between the orthogonalized spaces
    return np.linalg.svd(Qx.T @ Qy, compute_uv=False)


class NormFunction(Protocol):
    def __call__(
        self, x: ArrayLike, *, axis: SupportsIndex, keepdims: bool
    ) -> NDArray[np.floating]: ...


def normalize(
    X: ArrayLike, axis: int = -1, norm: NormFunction = np.linalg.norm
) -> NDArray[np.floating]:
    """Normalizes elements of an array or matrix.

    Args:
        X: The set of arrays to normalize.
        axis: The axis along which to compute the norm (Default: -1).
        norm: Function that computes the norm (Default: np.linalg.norm).

    Returns:
        Normalized array with the same shape as ``X``.

    Notes:
        Any vectors whose norm is zero remain zero after normalization instead of
        producing NaNs or infinities.
    """
    arr = np.asarray(X, dtype=float)
    denom = norm(arr, axis=axis, keepdims=True)
    zero_mask = denom == 0

    # Avoid divide-by-zero warnings and keep zeros in place by dividing only where safe.
    safe_denom = np.where(zero_mask, 1.0, denom)
    normalized = np.zeros_like(arr, dtype=float)
    np.divide(arr, safe_denom, out=normalized, where=~zero_mask)

    if np.any(zero_mask):
        normalized = np.where(zero_mask, 0.0, normalized)

    return normalized
