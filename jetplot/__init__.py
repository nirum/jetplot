"""Jetpack is a set of useful utility functions for scientific python."""

from . import colors as c
from .chart_utils import *
from .images import *
from .plots import *
from .style import *

from .signals import *
from .timepiece import *

from .version import __version__

light_mode()

try:
    set_font("Helvetica")
except ValueError:
    pass
