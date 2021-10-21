"""Image visualization tools."""

from functools import partial

import numpy as np
import matplotlib.pyplot as plt

from .chart_utils import noticks, plotwrapper

__all__ = ['img', 'imv', 'fsurface']


@plotwrapper
def img(data,
        mode='div',
        cmap=None,
        aspect='equal',
        vmin=None,
        vmax=None,
        cbar=True,
        interpolation='none',
        **kwargs):
  """Visualize a matrix as an image.

  Args:
    img: array_like, The array to visualize.
    mode: string, Either 'div' for a diverging image or 'seq' for
      sequential (default: 'div').
    cmap: string, Colormap to use.
    aspect: string, Either 'equal' or 'auto'
  """
  # work with a copy of the original image data
  img = np.squeeze(data.copy())

  # image bounds
  img_min = np.min(img)
  img_max = np.max(img)
  abs_max = np.max(np.abs(img))

  if mode == 'div':
    if vmin is None:
      vmin = -abs_max
    if vmax is None:
      vmax = abs_max
    if cmap is None:
      cmap = 'seismic'
  elif mode == 'seq':
    if vmin is None:
      vmin = img_min
    if vmax is None:
      vmax = img_max
    if cmap is None:
      cmap = 'viridis'
  elif mode == 'cov':
    vmin, vmax, cmap, cbar = 0, 1, 'viridis', True
  elif mode == 'cov':
    vmin, vmax, cmap, cbar = -1, 1, 'seismic', True
  else:
    raise ValueError("Unrecognized mode: '" + mode + "'")

  # make the image
  im = kwargs['ax'].imshow(img,
                           cmap=cmap,
                           interpolation=interpolation,
                           vmin=vmin,
                           vmax=vmax,
                           aspect=aspect)

  # colorbar
  if cbar:
    plt.colorbar(im)

  # clear ticks
  noticks(ax=kwargs['ax'])

  return im


@plotwrapper
def fsurface(func, xrng=None, yrng=None, n=100, nargs=2, **kwargs):
  xrng = (-1, 1) if xrng is None else xrng
  yrng = xrng if yrng is None else yrng

  xs = np.linspace(*xrng, n)
  ys = np.linspace(*yrng, n)

  xm, ym = np.meshgrid(xs, ys)

  if nargs == 1:
    zz = np.vstack((xm.ravel(), ym.ravel()))
    args = (zz,)
  elif nargs == 2:
    args = (xm.ravel(), ym.ravel())
  else:
    raise ValueError(f'Invalid value for nargs ({nargs})')

  zm = func(*args).reshape(xm.shape)

  kwargs['ax'].contourf(xm, ym, zm)


# aliases
imv = partial(img, mode='seq')
