"""Opinionated matplotlib style defaults."""

from functools import partial
from typing import Mapping, Any

from cycler import cycler
from jetplot.typing import Color, Palette
from matplotlib import font_manager as fm, rcParams

from . import colors as c

__all__ = [
    "STYLE_DEFAULTS",
    "set_defaults",
    "light_mode",
    "dark_mode",
    "set_font",
    "set_dpi",
    "available_fonts",
    "install_fonts",
]


STYLE_DEFAULTS = {
    "lines.linewidth": 1.5,
    "lines.linestyle": "-",
    "lines.marker": "",
    "lines.markeredgewidth": 0.0,
    "lines.markersize": 6.0,
    "lines.antialiased": True,
    "lines.solid_joinstyle": "round",
    "lines.solid_capstyle": "round",
    "patch.linewidth": 1.0,
    "patch.facecolor": "#cccccc",
    "patch.edgecolor": "none",
    "patch.antialiased": True,
    "font.size": 12,
    "text.usetex": False,
    "mathtext.default": "regular",
    "axes.linewidth": 1.0,
    "axes.grid": False,
    "axes.titlesize": 12,
    "axes.labelsize": 12,
    "axes.labelweight": "normal",
    "axes.axisbelow": True,
    "axes.formatter.use_mathtext": False,
    "axes.xmargin": 0.0,
    "axes.ymargin": 0.0,
    "polaraxes.grid": True,
    "xtick.direction": "out",
    "xtick.labelsize": 12.0,
    "xtick.major.size": 4.0,
    "xtick.minor.size": 2.0,
    "xtick.major.width": 1.0,
    "xtick.minor.width": 1.0,
    "ytick.direction": "out",
    "ytick.labelsize": 12.0,
    "ytick.major.size": 4.0,
    "ytick.minor.size": 2.0,
    "ytick.major.width": 1.0,
    "ytick.minor.width": 1.0,
    "grid.linestyle": "dotted",
    "grid.alpha": 0.5,
    "grid.linewidth": 1.0,
    "legend.frameon": False,
    "legend.fancybox": True,
    "legend.fontsize": 10.0,
    "legend.loc": "best",
    "figure.figsize": (5, 3),
    "figure.dpi": 150,
    "image.cmap": "viridis",
    "image.interpolation": "none",
    "image.aspect": "equal",
}


def set_colors(bg, fg, text):
    """Set background/foreground colorscheme."""
    rcParams.update(
        {
            "figure.facecolor": bg,
            "figure.edgecolor": bg,
            "axes.facecolor": bg,
            "savefig.facecolor": bg,
            "savefig.edgecolor": bg,
            "axes.edgecolor": fg,
            "axes.labelcolor": text,
            "xtick.color": fg,
            "ytick.color": fg,
            "legend.edgecolor": fg,
            "grid.color": fg,
            "text.color": text,
        }
    )


def set_font(fontname: str):
    """Specifies the matplotlib default font."""

    if fontname not in available_fonts():
        raise ValueError(f"Font {fontname} not found.")

    rcParams["font.family"] = fontname


def set_dpi(dpi: int):
    """Sets the figure DPI."""
    rcParams["figure.dpi"] = dpi


def set_defaults(
    *,
    bg: Color,
    fg: Color,
    text: Color,
    cycler_colors: Palette,
    defaults: Mapping[str, Any] = STYLE_DEFAULTS,
    font: str = "Helvetica",
):
    """Sets matplotlib defaults."""
    rcParams.update(defaults)
    set_colors(bg, fg, text)
    rcParams["axes.prop_cycle"] = cycler(color=cycler_colors)

    try:
        set_font(font)
    except ValueError:
        pass


light_mode = partial(
    set_defaults, bg=c.white, fg=c.gray[9], text=c.gray[9], cycler_colors=c.dark
)
dark_mode = partial(
    set_defaults, bg=c.black, fg=c.zinc[3], text=c.zinc[0], cycler_colors=c.bright
)


def available_fonts():
    return sorted(set([f.name for f in fm.fontManager.ttflist]))


def install_fonts(filepath: str):
    """Installs .ttf fonts in the given folder."""

    original_fonts = set(available_fonts())
    font_files = fm.findSystemFonts(fontpaths=[filepath])

    for font_file in font_files:
        fm.fontManager.addfont(font_file)

    new_fonts = set(available_fonts()) - original_fonts
    if new_fonts:
        print(f'Added the following fonts: {", ".join(new_fonts)}')
    else:
        print(f"No new fonts added.")
