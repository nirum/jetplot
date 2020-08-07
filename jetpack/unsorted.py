import re
import numpy as np
from .signals import norms


def fonts():
    import matplotlib.font_manager as fm
    return sorted(set([f.name for f in fm.fontManager.ttflist]))


def spherical_interp(x, y, t):
    """Spherical linear interpolation"""
    EPS = 1e-2

    xn, yn = norms(x), norms(y)

    theta = np.arccos(np.clip(np.inner(xn, yn), -1, 1))
    sin_theta = np.sin(theta)

    if sin_theta < EPS:
        c1 = 1 - t
        c2 = t
    else:
        c1 = np.sin((1 - t) * theta) / sin_theta
        c2 = np.sin(t * theta) / sin_theta

    return norms(c1 * x + c2 * y)


def alphanum_key(s):
    """Turn a string into a list of string and number chunks.
    
    Usage
    -----
    "z23a" -> ["z", 23, "a"]
    """
    def tryint(s):
        try:
            return int(s)
        except:
            return s

    return [tryint(c) for c in re.split('([0-9]+)', s)]


def humansort(arr):
    return sorted(arr, key=alphanum_key)
