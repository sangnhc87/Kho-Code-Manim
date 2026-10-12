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
