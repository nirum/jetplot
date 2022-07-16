from typing import Union, Sequence

__all__ = ['Color', 'Palette']

Color = Union[str, Sequence[float]]
Palette = Sequence[Color]
