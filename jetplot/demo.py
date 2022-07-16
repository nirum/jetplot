import numpy as np


def peaks(n=256):
    """2D peaks function."""
    pts = np.linspace(-3, 3, n)
    xm, ym = np.meshgrid(pts, pts)
    zm = 3 * (1 - xm) ** 2 * np.exp(-(xm ** 2)) - (ym + 1) ** 2 - 10 * (0.2 * xm - xm ** 3 - ym ** 5) * np.exp(-(xm ** 2) - (ym ** 2)) - (1/3) * np.exp(- (xm + 1) ** 2 - ym ** 2)
    return xm, ym, zm
