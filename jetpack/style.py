"""Opinionated matplotlib style defaults."""

from matplotlib import rcParams
import matplotlib.font_manager as fm


__all__ = ['light_mode', 'dark_mode']


rcParams.update({
    'lines.linewidth': 1.5,
    'lines.linestyle': '-',
    'lines.marker': None,
    'lines.markeredgewidth': 0.,
    'lines.markersize': 6.,
    'lines.antialiased': True,
    'lines.solid_joinstyle': 'round',
    'lines.solid_capstyle': 'round',

    'patch.linewidth': 1.,
    'patch.facecolor': '#cccccc',
    'patch.edgecolor': 'none',
    'patch.antialiased': True,

    'font.size': 12,
    'text.usetex': False,
    'mathtext.default': 'regular',

    'axes.linewidth': 1.0,
    'axes.grid': False,
    'axes.titlesize': 12,
    'axes.labelsize': 12,
    'axes.labelweight': 'normal',
    'axes.axisbelow': True,
    'axes.formatter.use_mathtext': False,
    'axes.xmargin': 0.,
    'axes.ymargin': 0.,
    'polaraxes.grid': True,

    'xtick.direction': 'out',
    'xtick.labelsize': 10.,
    'xtick.major.size': 4.,
    'xtick.minor.size': 2.,
    'xtick.major.width': 1.,
    'xtick.minor.width': 1.,

    'ytick.direction': 'out',
    'ytick.labelsize': 10.,
    'ytick.major.size': 4.,
    'ytick.minor.size': 2.,
    'ytick.major.width': 1.,
    'ytick.minor.width': 1.,

    'grid.linestyle': 'dotted',
    'grid.alpha': 0.5,
    'grid.linewidth': 1.0,

    'legend.frameon': False,
    'legend.fancybox': True,
    'legend.fontsize': 10.,
    'legend.loc': 'best',

    'figure.figsize': (5, 3),
    'figure.dpi': 100,
    'figure.autolayout': True,

    'image.cmap': 'turbo',
    'image.interpolation': None,
    'image.aspect': 'equal',

    'savefig.format': 'pdf',
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
    'pdf.fonttype': 42,
})


def set_colors(bg, fg, text):
  """Set background/foreground colorscheme."""
  rcParams.update({
      'figure.facecolor': bg,
      'figure.edgecolor': bg,
      'axes.facecolor': bg,
      'savefig.facecolor': bg,
      'savefig.edgecolor': bg,

      'axes.edgecolor': fg,
      'axes.labelcolor': fg,
      'xtick.color': fg,
      'ytick.color': fg,
      'legend.edgecolor': fg,

      'grid.color': fg,
      'text.color': text,
  })


def set_font(fontname):
  """Specifies the matplotlib default font."""
  assert fontname in available_fonts()
  rcParams.update({'font.family': fontname})


def light_mode():
  """Sets figure colors to have dark text on a light background."""
  set_colors('#ffffff', '#444444', '#222222')


def dark_mode():
  """Sets figure colors to have light text on a dark background."""
  set_colors('#000000', '#bbbbbb', '#dddddd')


def available_fonts():
    return sorted(set([f.name for f in fm.fontManager.ttflist]))
