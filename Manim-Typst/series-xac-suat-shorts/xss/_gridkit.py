"""Shared lattice helpers for the path / DP Shorts (XSS297+)."""
from __future__ import annotations

from manim import Dot, Line, VGroup, VMobject

from common.theme import STROKE, WHITE


class Lattice:
    def __init__(self, cols, rows, origin=(-1.8, -.1), step=1.0):
        self.cols, self.rows, self.o, self.s = cols, rows, origin, step

    def P(self, x, y):
        return [self.o[0] + self.s * x, self.o[1] + self.s * y, 0]

    def grid(self):
        lines = VGroup(*[Line(self.P(0, j), self.P(self.cols, j), color=STROKE, stroke_width=2) for j in range(self.rows + 1)],
                       *[Line(self.P(i, 0), self.P(i, self.rows), color=STROKE, stroke_width=2) for i in range(self.cols + 1)])
        dots = VGroup(*[Dot(self.P(i, j), radius=.06, color=WHITE) for i in range(self.cols + 1) for j in range(self.rows + 1)])
        return VGroup(lines, dots)

    def path(self, moves, color, width=6):
        pts, x, y = [self.P(0, 0)], 0, 0
        for m in moves:
            x, y = (x + 1, y) if m == 'R' else (x, y + 1)
            pts.append(self.P(x, y))
        v = VMobject(stroke_color=color, stroke_width=width)
        v.set_points_as_corners(pts)
        return v
