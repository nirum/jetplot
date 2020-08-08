"""Jetpack is a set of useful utility functions for scientific python."""

from .colors import *
from .style import *
from .chart_utils import *
from .plots import *
from .animation import *
from .images import *

from .signals import *
from .timepiece import *

from .version import __version__

light_mode()

try:
  set_font('Helvetica')
except ValueError:
  pass
