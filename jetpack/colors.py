"""Colorschemes."""

import matplotlib.cm as cm
import numpy as np


def cmap_colors(cmap, n, vmin=0, vmax=1):
  return cm.__getattribute__(cmap)(np.linspace(vmin, vmax, n))
