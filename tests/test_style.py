"""Tests style settings."""

import numpy as np
from matplotlib import rcParams

from jetplot import style


def test_defaults():
    for key in style.STYLE_DEFAULTS.keys():
        assert key in rcParams


def test_light_mode():
    style.light_mode()
    for key, value in style.STYLE_DEFAULTS.items():
        if isinstance(value, tuple):
            assert np.allclose(rcParams[key], value)
        else:
            assert rcParams[key] == value


def test_dark_mode():
    style.dark_mode()
    for key, value in style.STYLE_DEFAULTS.items():
        if isinstance(value, tuple):
            assert np.allclose(rcParams[key], value)
        else:
            assert rcParams[key] == value
