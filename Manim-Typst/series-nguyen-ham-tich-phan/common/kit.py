"""Visual building blocks for the INT series (no LaTeX: Text + Typst SVG only)."""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from manim import (DOWN, LEFT, ORIGIN, RIGHT, UP, Arc, Axes, Circle, Dot, Line, Polygon,
                   RoundedRectangle, Text, VGroup, VMobject, always_redraw, SVGMobject)

from common.theme import (CYAN, DIM, FONT, GOLD, GREEN, MATH_SCALE, PANEL_2, SOFT, STROKE,
                          WHITE, CORAL)


# ------------------------------------------------------------------ text
def tx(s, size=24, color=WHITE, bold=False, max_w=None, slant=False):
    m = Text(str(s), font=FONT, font_size=size, color=color,
             weight='BOLD' if bold else 'NORMAL', slant='ITALIC' if slant else 'NORMAL')
    if max_w is not None and m.width > max_w:
        m.scale_to_fit_width(max_w)
    return m


def para(s, size=24, color=WHITE, width=40, buff=0.16, bold=False, max_w=None, center=False):
    """Paragraph wrapped at ``width`` characters (left-aligned unless ``center``)."""
    import textwrap
    lines = textwrap.wrap(str(s), width=width, break_long_words=False) or ['']
    g = VGroup(*[tx(line, size, color, bold) for line in lines])
    g.arrange(DOWN, buff=buff) if center else g.arrange(DOWN, buff=buff, aligned_edge=LEFT)
    if max_w is not None and g.width > max_w:
        g.scale_to_fit_width(max_w)
    return g


def vn(v, nd=2):
    """Vietnamese decimal comma."""
    s = f'{v:.{nd}f}'
    if s.startswith('-'):
        s = '−' + s[1:]
    return s.replace('.', ',')


BAR_WIDTH = 1.9  # Manim stroke width of a fraction bar at scale 1


class Formula:
    """Loads Typst-compiled SVGs at a fixed physical scale (consistent sizes)."""

    def __init__(self, directory: Path):
        self.dir = Path(directory)

    def __call__(self, key, scale=1.0, max_w=None):
        path = self.dir / f'{key}.svg'
        if not path.exists():
            raise FileNotFoundError(f'Typst asset not compiled: {path} (run scripts/build_typst.py)')
        m = SVGMobject(str(path), height=None, width=None)
        m.scale(MATH_SCALE * scale)
        # Typst draws fraction bars / radical overlines as stroked paths: keep
        # them (scaled to the glyph size); glyphs themselves are fill only.
        for part in m.family_members_with_points():
            if part.get_fill_opacity() < .01 and part.get_stroke_width() > 0:
                part.set_stroke(width=BAR_WIDTH * scale)
            else:
                part.set_stroke(width=0)
        if max_w is not None and m.width > max_w:
            m.scale_to_fit_width(max_w)
        return m


# ------------------------------------------------------------------ graphs
def axes(x_range, y_range, width, height, center=ORIGIN, x_ticks=(), y_ticks=(),
         x_label='x', y_label='y', label_size=17):
    a = Axes(x_range=list(x_range), y_range=list(y_range), x_length=width, y_length=height,
             tips=True,
             axis_config={'color': SOFT, 'stroke_width': 2, 'tip_width': 0.16, 'tip_height': 0.16,
                          'include_ticks': False})
    a.move_to(center)
    labels = VGroup()
    for v in x_ticks:
        p = a.c2p(v, 0)
        labels.add(Line(p + UP * .06, p + DOWN * .06, color=SOFT, stroke_width=2))
        labels.add(tx(vn(v, 0) if float(v).is_integer() else vn(v, 1), label_size, SOFT).move_to(p + DOWN * .27))
    for v in y_ticks:
        p = a.c2p(0, v)
        labels.add(Line(p + LEFT * .06, p + RIGHT * .06, color=SOFT, stroke_width=2))
        labels.add(tx(vn(v, 0) if float(v).is_integer() else vn(v, 1), label_size, SOFT).next_to(p, LEFT, buff=.12))
    if x_label:
        labels.add(tx(x_label, label_size + 2, SOFT, slant=True).next_to(a.x_axis.get_end(), DOWN, buff=.14))
    if y_label:
        labels.add(tx(y_label, label_size + 2, SOFT, slant=True).next_to(a.y_axis.get_end(), LEFT, buff=.14))
    a.labels = labels
    return a


def clipped(a, f, x0, x1, color=CYAN, width=4.0, n=320, y_min=None, y_max=None):
    """Graph of f on [x0, x1] restricted to the visible y-range (clean edges, no overflow)."""
    lo = a.y_range[0] if y_min is None else y_min
    hi = a.y_range[1] if y_max is None else y_max
    group = VGroup()
    seg = []

    def value(xv):
        try:
            return float(f(xv))
        except (ZeroDivisionError, ValueError, OverflowError):
            return math.nan

    def flush():
        if len(seg) >= 2:
            m = VMobject(stroke_color=color, stroke_width=width)
            m.set_points_as_corners([a.c2p(px, py) for px, py in seg])
            group.add(m)
        seg.clear()

    prev = None
    for xv in np.linspace(x0, x1, n):
        yv = value(xv)
        inside = math.isfinite(yv) and lo <= yv <= hi
        if prev is not None:
            px, py = prev
            pin = math.isfinite(py) and lo <= py <= hi
            if inside != pin and math.isfinite(py) and math.isfinite(yv):
                bound = hi if max(py, yv) > hi else lo
                seg.append((px + (bound - py) * (xv - px) / (yv - py), bound))
                if pin:
                    flush()
            elif not math.isfinite(yv):
                flush()
        if inside:
            seg.append((xv, yv))
        prev = (xv, yv)
    flush()
    return group


def screen_dir(a, x0, y0, slope):
    p = a.c2p(x0, y0)
    q = a.c2p(x0 + 1.0, y0 + slope)
    d = q - p
    return d / np.linalg.norm(d)


def slope_field(a, slope, xs, ys, seg=0.30, color=SOFT, width=2.0, opacity=0.75):
    g = VGroup()
    for xv in xs:
        for yv in ys:
            p = a.c2p(xv, yv)
            d = screen_dir(a, xv, yv, slope(xv, yv)) * seg / 2
            g.add(Line(p - d, p + d, color=color, stroke_width=width, stroke_opacity=opacity))
    return g


def tangent(a, x0, y0, slope, length=1.8, color=GOLD, width=3.2):
    p = a.c2p(x0, y0)
    d = screen_dir(a, x0, y0, slope) * length / 2
    return Line(p - d, p + d, color=color, stroke_width=width)


def dashed(p, q, **kw):
    """DashedLine that tolerates zero length (used inside always_redraw)."""
    from manim import DashedLine
    p, q = np.array(p, dtype=float), np.array(q, dtype=float)
    if np.linalg.norm(q - p) < 1e-3:
        return Line(p, p + np.array([1e-3, 0, 0]), stroke_opacity=0)
    return DashedLine(p, q, **kw)


def dot(a, x0, y0, color=GOLD, r=0.075):
    return Dot(a.c2p(x0, y0), radius=r, color=color)


# ------------------------------------------------------------------ props
def car(color=CORAL, scale=1.0):
    body = RoundedRectangle(width=1.2, height=0.36, corner_radius=0.1, fill_color=color, fill_opacity=1,
                            stroke_width=0)
    cabin = Polygon([-0.33, 0.18, 0], [-0.18, 0.44, 0], [0.24, 0.44, 0], [0.4, 0.18, 0],
                    fill_color=color, fill_opacity=1, stroke_width=0)
    window = Polygon([-0.24, 0.2, 0], [-0.13, 0.38, 0], [0.2, 0.38, 0], [0.31, 0.2, 0],
                     fill_color='#0B1221', fill_opacity=0.85, stroke_width=0)
    w1 = Circle(radius=0.12, fill_color='#1B2436', fill_opacity=1, stroke_color=WHITE, stroke_width=2).move_to([-0.34, -0.2, 0])
    w2 = w1.copy().move_to([0.34, -0.2, 0])
    g = VGroup(body, cabin, window, w1, w2)
    g.scale(scale)
    return g


def gauge(value_fn, vmax, center, radius=1.0, unit='m/s', color=CYAN):
    """Speedometer whose needle follows value_fn() (an always_redraw)."""
    a0, a1 = 210 * math.pi / 180, -30 * math.pi / 180
    arc = Arc(radius=radius, start_angle=a0, angle=a1 - a0, color=STROKE, stroke_width=10).move_arc_center_to(center)
    ticks = VGroup()
    for k in range(int(vmax) + 1):
        ang = a0 + (a1 - a0) * k / vmax
        u = np.array([math.cos(ang), math.sin(ang), 0])
        ticks.add(Line(center + u * (radius - .16), center + u * (radius - .02), color=SOFT, stroke_width=2))
        if k % 2 == 0:
            ticks.add(tx(str(k), 15, SOFT).move_to(center + u * (radius - .36)))

    def needle():
        v = max(0.0, min(vmax, value_fn()))
        ang = a0 + (a1 - a0) * v / vmax
        u = np.array([math.cos(ang), math.sin(ang), 0])
        return VGroup(Line(center, center + u * (radius - .2), color=GOLD, stroke_width=5),
                      Dot(center, radius=.07, color=GOLD))

    readout = always_redraw(lambda: tx(f'{vn(value_fn(), 1)} {unit}', 22, color, bold=True)
                            .move_to(center + DOWN * radius * .55))
    return VGroup(arc, ticks, always_redraw(needle), readout)


def card(width, height, stroke=STROKE, fill=PANEL_2, radius=0.16, opacity=1.0, stroke_width=1.6):
    return RoundedRectangle(width=width, height=height, corner_radius=radius, fill_color=fill,
                            fill_opacity=opacity, stroke_color=stroke, stroke_width=stroke_width)


def check(color=GREEN, size=0.32):
    m = VMobject(stroke_color=color, stroke_width=6)
    m.set_points_as_corners([[-0.5, 0.0, 0], [-0.15, -0.38, 0], [0.55, 0.42, 0]])
    return m.scale(size / 0.9)


def cross(color=CORAL, size=0.3):
    s = size / 2
    return VGroup(Line([-s, -s, 0], [s, s, 0], color=color, stroke_width=6),
                  Line([-s, s, 0], [s, -s, 0], color=color, stroke_width=6))


def badge(text, color=GREEN, size=18, pad=0.14):
    label = tx(text, size, '#0B1221', bold=True)
    box = RoundedRectangle(width=label.width + 2 * pad + .1, height=label.height + 2 * pad,
                           corner_radius=0.1, fill_color=color, fill_opacity=1, stroke_width=0)
    return VGroup(box, label.move_to(box))


def underline(m, color=GOLD, buff=0.08, width=3):
    return Line(m.get_corner(DOWN + LEFT) + DOWN * buff, m.get_corner(DOWN + RIGHT) + DOWN * buff,
                color=color, stroke_width=width)


__all__ = ['tx', 'para', 'vn', 'Formula', 'axes', 'clipped', 'slope_field', 'tangent', 'dot', 'car',
           'gauge', 'card', 'dashed', 'check', 'cross', 'badge', 'underline', 'screen_dir',
           'CYAN', 'DIM', 'GOLD', 'GREEN', 'SOFT', 'WHITE', 'CORAL']
