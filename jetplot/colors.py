"""Colorschemes"""

from matplotlib import cm, pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_hex
import numpy as np

from .chart_utils import noticks

__all__ = ["Palette", "cubehelix", "cmap_colors"]


class Palette(list):
    """Color palette."""

    @property
    def hex(self):
        return Palette([to_hex(rgb) for rgb in self])

    @property
    def cmap(self):
        return LinearSegmentedColormap.from_list("", self)

    def plot(self, figsize=(5, 1)):
        fig, axs = plt.subplots(1, len(self), figsize=figsize)
        for c, ax in zip(self, axs):
            ax.set_facecolor(c)
            ax.set_aspect("equal")
            noticks(ax=ax)

        return fig, axs


def cubehelix(
    n: int, vmin=0.85, vmax=0.15, gamma: float = 1.0, start=0.0, rot=0.4, hue=0.8
):
    """Cubehelix parameterized colormap."""
    lambda_ = np.linspace(vmin, vmax, n)
    x = lambda_ ** gamma
    phi = 2 * np.pi * (start / 3 + rot * lambda_)
    alpha = 0.5 * hue * x * (1.0 - x)
    A = np.array([[-0.14861, 1.78277], [-0.29227, -0.90649], [1.97294, 0.0]])
    b = np.stack([np.cos(phi), np.sin(phi)])
    return Palette((x + alpha * (A @ b)).T)


def cmap_colors(cmap: str, n: int, vmin: float = 0.0, vmax: float = 1.0):
    return Palette(cm.__getattribute__(cmap)(np.linspace(vmin, vmax, n)))


black = "#000000"
white = "#ffffff"
slate = Palette(
    [
        "#F8FAFC",
        "#F1F5F9",
        "#E2E8F0",
        "#CBD5E1",
        "#94A3B8",
        "#64748B",
        "#475569",
        "#334155",
        "#1E293B",
        "#0F172A",
    ]
)
gray = Palette(
    [
        "#F9FAFB",
        "#F3F4F6",
        "#E5E7EB",
        "#D1D5DB",
        "#9CA3AF",
        "#6B7280",
        "#4B5563",
        "#374151",
        "#1F2937",
        "#111827",
    ]
)
zinc = Palette(
    [
        "#FAFAFA",
        "#F4F4F5",
        "#E4E4E7",
        "#D4D4D8",
        "#A1A1AA",
        "#71717A",
        "#52525B",
        "#3F3F46",
        "#27272A",
        "#18181B",
    ]
)
neutral = Palette(
    [
        "#FAFAFA",
        "#F5F5F5",
        "#E5E5E5",
        "#D4D4D4",
        "#A3A3A3",
        "#737373",
        "#525252",
        "#404040",
        "#262626",
        "#171717",
    ]
)
stone = Palette(
    [
        "#FAFAF9",
        "#F5F5F4",
        "#E7E5E4",
        "#D6D3D1",
        "#A8A29E",
        "#78716C",
        "#57534E",
        "#44403C",
        "#292524",
        "#1C1917",
    ]
)
red = Palette(
    [
        "#FEF2F2",
        "#FEE2E2",
        "#FECACA",
        "#FCA5A5",
        "#F87171",
        "#EF4444",
        "#DC2626",
        "#B91C1C",
        "#991B1B",
        "#7F1D1D",
    ]
)
orange = Palette(
    [
        "#FFF7ED",
        "#FFEDD5",
        "#FED7AA",
        "#FDBA74",
        "#FB923C",
        "#F97316",
        "#EA580C",
        "#C2410C",
        "#9A3412",
        "#7C2D12",
    ]
)
amber = Palette(
    [
        "#FFFBEB",
        "#FEF3C7",
        "#FDE68A",
        "#FCD34D",
        "#FBBF24",
        "#F59E0B",
        "#D97706",
        "#B45309",
        "#92400E",
        "#78350F",
    ]
)
yellow = Palette(
    [
        "#FEFCE8",
        "#FEF9C3",
        "#FEF08A",
        "#FDE047",
        "#FACC15",
        "#EAB308",
        "#CA8A04",
        "#A16207",
        "#854D0E",
        "#713F12",
    ]
)
lime = Palette(
    [
        "#F7FEE7",
        "#ECFCCB",
        "#D9F99D",
        "#BEF264",
        "#A3E635",
        "#84CC16",
        "#65A30D",
        "#4D7C0F",
        "#3F6212",
        "#365314",
    ]
)
green = Palette(
    [
        "#F0FDF4",
        "#DCFCE7",
        "#BBF7D0",
        "#86EFAC",
        "#4ADE80",
        "#22C55E",
        "#16A34A",
        "#15803D",
        "#166534",
        "#14532D",
    ]
)
emerald = Palette(
    [
        "#ECFDF5",
        "#D1FAE5",
        "#A7F3D0",
        "#6EE7B7",
        "#34D399",
        "#10B981",
        "#059669",
        "#047857",
        "#065F46",
        "#064E3B",
    ]
)
teal = Palette(
    [
        "#F0FDFA",
        "#CCFBF1",
        "#99F6E4",
        "#5EEAD4",
        "#2DD4BF",
        "#14B8A6",
        "#0D9488",
        "#0F766E",
        "#115E59",
        "#134E4A",
    ]
)
cyan = Palette(
    [
        "#ECFEFF",
        "#CFFAFE",
        "#A5F3FC",
        "#67E8F9",
        "#22D3EE",
        "#06B6D4",
        "#0891B2",
        "#0E7490",
        "#155E75",
        "#164E63",
    ]
)
sky = Palette(
    [
        "#F0F9FF",
        "#E0F2FE",
        "#BAE6FD",
        "#7DD3FC",
        "#38BDF8",
        "#0EA5E9",
        "#0284C7",
        "#0369A1",
        "#075985",
        "#0C4A6E",
    ]
)
blue = Palette(
    [
        "#EFF6FF",
        "#DBEAFE",
        "#BFDBFE",
        "#93C5FD",
        "#60A5FA",
        "#3B82F6",
        "#2563EB",
        "#1D4ED8",
        "#1E40AF",
        "#1E3A8A",
    ]
)
indigo = Palette(
    [
        "#EEF2FF",
        "#E0E7FF",
        "#C7D2FE",
        "#A5B4FC",
        "#818CF8",
        "#6366F1",
        "#4F46E5",
        "#4338CA",
        "#3730A3",
        "#312E81",
    ]
)
violet = Palette(
    [
        "#F5F3FF",
        "#EDE9FE",
        "#DDD6FE",
        "#C4B5FD",
        "#A78BFA",
        "#8B5CF6",
        "#7C3AED",
        "#6D28D9",
        "#5B21B6",
        "#4C1D95",
    ]
)
purple = Palette(
    [
        "#FAF5FF",
        "#F3E8FF",
        "#E9D5FF",
        "#D8B4FE",
        "#C084FC",
        "#A855F7",
        "#9333EA",
        "#7E22CE",
        "#6B21A8",
        "#581C87",
    ]
)
fuchsia = Palette(
    [
        "#FDF4FF",
        "#FAE8FF",
        "#F5D0FE",
        "#F0ABFC",
        "#E879F9",
        "#D946EF",
        "#C026D3",
        "#A21CAF",
        "#86198F",
        "#701A75",
    ]
)
pink = Palette(
    [
        "#FDF2F8",
        "#FCE7F3",
        "#FBCFE8",
        "#F9A8D4",
        "#F472B6",
        "#EC4899",
        "#DB2777",
        "#BE185D",
        "#9D174D",
        "#831843",
    ]
)
rose = Palette(
    [
        "#FFF1F2",
        "#FFE4E6",
        "#FECDD3",
        "#FDA4AF",
        "#FB7185",
        "#F43F5E",
        "#E11D48",
        "#BE123C",
        "#9F1239",
        "#881337",
    ]
)

def rainbow(k: int) -> Palette:
    _colors = (blue, orange, green, red, purple, teal, pink, indigo, emerald, rose, lime, sky, amber)
    return Palette([r[k] for r in _colors])

bright: Palette = rainbow(4)
dark: Palette = rainbow(6)
