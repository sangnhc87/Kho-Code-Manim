"""Shared regular-polygon helpers for the conditional-geometry Shorts (XSS313+)."""
from __future__ import annotations

from itertools import combinations

from manim import Dot, FadeIn, FadeOut, Polygon, VGroup

from common.theme import GOLD, STROKE, WHITE
from common.visuals import polygon_pts


def arcs(t, n):
    """Arc gaps (in edges) between consecutive chosen vertices; angles of the triangle are π·gap/n."""
    a, b, c = sorted(t)
    return b - a, c - b, n - c + a


def triangles(n, cond=lambda t: True):
    return [t for t in combinations(range(n), 3) if cond(t)]


def is_right(n):
    return lambda t: 2 * max(arcs(t, n)) == n


def is_obtuse(n):
    return lambda t: 2 * max(arcs(t, n)) > n


def is_iso(n):
    return lambda t: len(set(arcs(t, n))) < 3


class PolyMixin:
    def show_ngon(self, n, r=2.0, center=(0, .9), frac=.08):
        self.pts = polygon_pts(n, r, center)
        self.ngon = VGroup(Polygon(*self.pts, stroke_color=STROKE, stroke_width=4),
                           VGroup(*[Dot(p, radius=.09, color=WHITE) for p in self.pts]))
        self.play(FadeIn(self.ngon), run_time=self.rt(frac))
        return self.ngon

    def shape(self, idx, color=GOLD, op=.35):
        return Polygon(*[self.pts[i] for i in idx], stroke_color=color, stroke_width=6, fill_color=color, fill_opacity=op)

    def flash(self, groups, color=GOLD, total=.3):
        """Show a few vertex tuples one after another, keeping the last one on screen."""
        cur = None
        step = total / max(len(groups), 1)
        for g in groups:
            new = self.shape(g, color)
            self.play(*([FadeOut(cur)] if cur else []), FadeIn(new), run_time=self.rt(step))
            cur = new
        return cur


CUBE = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]


def d2(a, b):
    return sum((i - j) ** 2 for i, j in zip(a, b))


def cube_view(v, s=1.9, o=(-1.25, -.2)):
    """Oblique projection of a unit-cube vertex."""
    return [o[0] + s * v[0] + .85 * v[2], o[1] + s * v[1] + .7 * v[2], 0]


def cube_mob():
    from manim import Line
    edges = VGroup(*[Line(cube_view(a), cube_view(b), color=STROKE, stroke_width=3)
                     for a, b in combinations(CUBE, 2) if d2(a, b) == 1])
    dots = VGroup(*[Dot(cube_view(v), radius=.11, color=WHITE) for v in CUBE])
    return VGroup(edges, dots)
