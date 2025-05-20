from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

__all__ = ["Color", "Palette", "FloatArray"]

Color = str | Sequence[float]
Palette = Sequence[Color]

FloatArray = NDArray[np.floating]
