"""Solids of revolution drawn in 2D (INT26–INT28).

The profile y = ±f(x) plus thin ellipses (discs seen slightly from the side);
rotation is suggested by squashing the region with cos θ.
"""
from __future__ import annotations

from manim import Ellipse, Polygon, VGroup

from common.kit import clipped
from common.theme import BG, CYAN, GOLD, WHITE

TILT = .28  # ellipse width / height (how much of the disc face we see)


def region(a, f, x0, x1, squash=1.0, color=CYAN, opacity=.45, samples=60, g=None):
    """Region under f (or between f and g) on [x0, x1], heights scaled by ``squash``."""
    xs = [x0 + (x1 - x0) * k / samples for k in range(samples + 1)]
    top = [a.c2p(v, squash * f(v)) for v in xs]
    bottom = [a.c2p(v, squash * g(v)) for v in xs[::-1]] if g else [a.c2p(x1, 0), a.c2p(x0, 0)]
    return Polygon(*top, *bottom, stroke_width=0, fill_color=color, fill_opacity=opacity)


def _radius(a, value):
    return abs(a.c2p(0, abs(value))[1] - a.c2p(0, 0)[1])


def disc(a, f, xv, color=GOLD, opacity=.55, stroke=1.6):
    r = _radius(a, f(xv))
    return Ellipse(width=max(2 * r * TILT, .02), height=max(2 * r, .02), color=WHITE, stroke_width=stroke,
                   fill_color=color, fill_opacity=opacity).move_to(a.c2p(xv, 0))


def ring(a, f, g, xv, color=GOLD, opacity=.6, stroke=1.6):
    """Washer at x: outer radius |f|, inner radius |g| (hole painted with the background)."""
    outer = disc(a, f, xv, color, opacity, stroke)
    ri = _radius(a, g(xv))
    hole = Ellipse(width=max(2 * ri * TILT, .01), height=max(2 * ri, .01), color=WHITE, stroke_width=stroke,
                   fill_color=BG, fill_opacity=1).move_to(a.c2p(xv, 0))
    return VGroup(outer, hole)


def solid(a, f, x0, x1, n=14, color=CYAN):
    """Profile ±f plus a row of translucent discs."""
    top = clipped(a, f, x0, x1, color, 3.5)
    bot = clipped(a, lambda v: -f(v), x0, x1, color, 3.5)
    discs = VGroup(*[disc(a, f, x0 + (x1 - x0) * (k + .5) / n, color, .18, 1) for k in range(n)])
    return VGroup(discs, top, bot, disc(a, f, x1, color, .3, 2))
