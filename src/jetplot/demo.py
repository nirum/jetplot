import numpy as np
from numpy.typing import NDArray


def peaks(n: int = 256) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """Generate the MATLAB ``peaks`` surface.

    Parameters
    ----------
    n:
        Number of points per axis.

    Returns
    -------
    tuple of ``ndarray``
        ``x`` grid, ``y`` grid and the function value ``z``.
    """

    pts = np.linspace(-3.0, 3.0, n)
    xm, ym = np.meshgrid(pts, pts, indexing="xy")
    zm = (
        3 * (1 - xm) ** 2 * np.exp(-(xm**2))
        - (ym + 1) ** 2
        - 10 * (0.2 * xm - xm**3 - ym**5) * np.exp(-(xm**2) - (ym**2))
        - (1.0 / 3.0) * np.exp(-((xm + 1) ** 2) - ym**2)
    )
    return xm, ym, zm
