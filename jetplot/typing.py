from typing import Sequence, Union

__all__ = ["Color", "Palette"]

Color = Union[str, Sequence[float]]
Palette = Sequence[Color]
