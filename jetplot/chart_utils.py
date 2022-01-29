"""Plotting utils."""

import numpy as np
import matplotlib.pyplot as plt

from functools import wraps

__all__ = ['noticks', 'nospines', 'breathe', 'plotwrapper', 'axwrapper',
           'get_bounds', 'yclamp', 'xclamp']


def plotwrapper(fun):
 """Decorator that adds figure and axes handles to the kwargs of a function."""
 @wraps(fun)
 def wrapper(*args, **kwargs):

  if 'ax' not in kwargs:
    if 'fig' not in kwargs:
      figsize = kwargs['figsize'] if 'figsize' in kwargs else None
      kwargs['fig'] = plt.figure(figsize=figsize)
    kwargs['ax'] = kwargs['fig'].add_subplot(111)
  else:
    if 'fig' not in kwargs:
      kwargs['fig'] = kwargs['ax'].get_figure()

  return fun(*args, **kwargs)
 return wrapper


def axwrapper(fun):
  """Decorator that adds an axes handle to kwargs."""
  @wraps(fun)
  def wrapper(*args, **kwargs):
    if 'ax' not in kwargs:
      if 'fig' not in kwargs:
        kwargs['fig'] = plt.gcf()
      kwargs['ax'] = plt.gca()
    else:
      if 'fig' not in kwargs:
        kwargs['fig'] = kwargs['ax'].get_figure()
    return fun(*args, **kwargs)
  return wrapper


@axwrapper
def noticks(**kwargs):
  """
  Clears tick marks (useful for images)
  """

  ax = kwargs['ax']
  ax.set_xticks([])
  ax.set_yticks([])


@axwrapper
def nospines(left=False, bottom=False, top=True, right=True, **kwargs):
  """
  Hides the specified axis spines (by default, right and top spines)
  """

  ax = kwargs['ax']

  # assemble args into dict
  disabled = dict(left=left, right=right, top=top, bottom=bottom)

  # disable spines
  for key in disabled:
    if disabled[key]:
      ax.spines[key].set_color('none')

  # disable xticks
  if disabled['top'] and disabled['bottom']:
    ax.set_xticks([])
  elif disabled['top']:
    ax.xaxis.set_ticks_position('bottom')
  elif disabled['bottom']:
    ax.xaxis.set_ticks_position('top')

  # disable yticks
  if disabled['left'] and disabled['right']:
    ax.set_yticks([])
  elif disabled['left']:
    ax.yaxis.set_ticks_position('right')
  elif disabled['right']:
    ax.yaxis.set_ticks_position('left')

  return ax


def get_bounds(axis, ax=None):
  if ax is None:
    ax = plt.gca()

  axis_map = {
      "x": (ax.get_xticks, ax.get_xticklabels, ax.get_xlim, "bottom"),
      "y": (ax.get_yticks, ax.get_yticklabels, ax.get_ylim, "left"),
  }

  # get functions
  ticks, labels, limits, spine_key = axis_map[axis]

  if ax.spines[spine_key].get_bounds():
    return ax.spines[spine_key].get_bounds()
  else:
    lower, upper = None, None
    for tick, label in zip(ticks(), labels()):
      if label.get_text() != '':
        if lower is None:
          lower = tick
        else:
          upper = tick

    if lower is None or upper is None:
      return limits()

  return lower, upper


@axwrapper
def breathe(xlims=None, ylims=None, padding_percent=0.05, **kwargs):
  """Adds space between axes and plot."""
  ax = kwargs['ax']

  if ax.get_xscale() == 'log':
    xfwd = np.log10
    xrev = lambda x: 10 ** x
  else:
    xfwd = lambda x: x
    xrev = lambda x: x

  if ax.get_yscale() == 'log':
    yfwd = np.log10
    yrev = lambda x: 10 ** x
  else:
    yfwd = lambda x: x
    yrev = lambda x: x

  xmin, xmax = xfwd(ax.get_xlim()) if xlims is None else xlims
  ymin, ymax = yfwd(ax.get_ylim()) if ylims is None else ylims

  xdelta = (xmax - xmin) * padding_percent
  ydelta = (ymax - ymin) * padding_percent

  ax.set_xlim(xrev(xmin - xdelta), xrev(xmax + xdelta))
  ax.spines['bottom'].set_bounds(xrev(xmin), xrev(xmax))

  ax.set_ylim(yrev(ymin - ydelta), yrev(ymax + ydelta))
  ax.spines['left'].set_bounds(yrev(ymin), yrev(ymax))

  nospines(**kwargs)

  return ax


@axwrapper
def yclamp(y0=None, y1=None, dt=None, **kwargs):
  ax = kwargs['ax']

  lims = ax.get_ylim()
  y0 = lims[0] if y0 is None else y0
  y1 = lims[1] if y1 is None else y1
  dt = np.mean(np.diff(ax.get_yticks())) if dt is None else dt
  print('hello world')

  new_ticks = np.arange(dt * np.floor(y0 / dt), dt * (np.ceil(y1 / dt) + 1), dt)
  ax.set_yticks(new_ticks)
  ax.set_yticklabels(new_ticks)
  ax.set_ylim(new_ticks[0], new_ticks[1])

  return ax


@axwrapper
def xclamp(x0=None, x1=None, dt=None, **kwargs):
  ax = kwargs['ax']

  lims = ax.get_xlim()
  x0 = lims[0] if x0 is None else x0
  x1 = lims[1] if x1 is None else x1
  dt = np.mean(np.diff(ax.get_xticks())) if dt is None else dt

  new_ticks = np.arange(dt * np.floor(x0 / dt), dt * (np.ceil(x1 / dt) + 1), dt)
  ax.set_xticks(new_ticks)
  ax.set_xticklabels(new_ticks)
  ax.set_xlim(new_ticks[0], new_ticks[1])

  return ax
