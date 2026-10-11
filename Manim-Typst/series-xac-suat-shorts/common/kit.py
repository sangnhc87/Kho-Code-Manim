"""Small drawing helpers shared by every Short (no LaTeX: Text + Typst SVG only)."""
from __future__ import annotations

import textwrap
from pathlib import Path

from manim import DOWN, LEFT, Line, RoundedRectangle, SVGMobject, Text, VGroup, VMobject

from common.theme import CORAL, FONT, GREEN, INK, MATH_SCALE, PANEL_2, STROKE, WHITE

BAR_WIDTH = 1.9  # Manim stroke width of a Typst fraction bar at scale 1


def tx(s, size=24, color=WHITE, bold=False, max_w=None, slant=False):
    m = Text(str(s), font=FONT, font_size=size, color=color,
             weight='BOLD' if bold else 'NORMAL', slant='ITALIC' if slant else 'NORMAL')
    if max_w is not None and m.width > max_w:
        m.scale_to_fit_width(max_w)
    return m


def para(s, size=24, color=WHITE, width=30, buff=0.14, bold=False, max_w=None, center=True):
    lines = textwrap.wrap(str(s), width=width, break_long_words=False) or ['']
    g = VGroup(*[tx(line, size, color, bold) for line in lines])
    g.arrange(DOWN, buff=buff) if center else g.arrange(DOWN, buff=buff, aligned_edge=LEFT)
    if max_w is not None and g.width > max_w:
        g.scale_to_fit_width(max_w)
    return g


def vn(v, nd=2):
    s = f'{v:.{nd}f}'
    if s.startswith('-'):
        s = '−' + s[1:]
    return s.replace('.', ',')


class Formula:
    """Loads Typst-compiled SVGs at a fixed physical scale."""

    def __init__(self, directory: Path):
        self.dir = Path(directory)

    def __call__(self, key, scale=1.0, max_w=None, color=None):
        path = self.dir / f'{key}.svg'
        if not path.exists():
            raise FileNotFoundError(f'Typst asset not compiled: {path} (run scripts/build_typst.py)')
        m = SVGMobject(str(path), height=None, width=None)
        m.scale(MATH_SCALE * scale)
        for part in m.family_members_with_points():
            if part.get_fill_opacity() < .01 and part.get_stroke_width() > 0:
                part.set_stroke(width=BAR_WIDTH * scale)
            else:
                part.set_stroke(width=0)
        if max_w is not None and m.width > max_w:
            m.scale_to_fit_width(max_w)
        return m


def card(width, height, stroke=STROKE, fill=PANEL_2, radius=0.18, opacity=1.0, stroke_width=2):
    return RoundedRectangle(width=width, height=height, corner_radius=radius, fill_color=fill,
                            fill_opacity=opacity, stroke_color=stroke, stroke_width=stroke_width)


def badge(text, color=GREEN, size=20, pad=0.14):
    label = tx(text, size, INK, bold=True)
    box = RoundedRectangle(width=label.width + 2 * pad + .1, height=label.height + 2 * pad,
                           corner_radius=0.1, fill_color=color, fill_opacity=1, stroke_width=0)
    return VGroup(box, label.move_to(box))


def check(color=GREEN, size=0.4):
    m = VMobject(stroke_color=color, stroke_width=7)
    m.set_points_as_corners([[-0.5, 0.0, 0], [-0.15, -0.38, 0], [0.55, 0.42, 0]])
    return m.scale(size / 0.9)


def cross(color=CORAL, size=0.36):
    s = size / 2
    return VGroup(Line([-s, -s, 0], [s, s, 0], color=color, stroke_width=7),
                  Line([-s, s, 0], [s, -s, 0], color=color, stroke_width=7))


__all__ = ['tx', 'para', 'vn', 'Formula', 'card', 'badge', 'check', 'cross', 'LEFT']
