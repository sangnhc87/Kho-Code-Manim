"""Unit-square helpers for the 2-D geometric-probability Shorts (XSS315+)."""
from __future__ import annotations

from manim import DOWN, LEFT, Polygon, Square, VGroup

from common.theme import SOFT, STROKE


class Unit:
    def __init__(self, side=3.4, origin=(-1.7, -1.25)):
        self.s, self.o = side, origin

    def P(self, x, y):
        return [self.o[0] + self.s * x, self.o[1] + self.s * y, 0]

    def frame(self, scene, xl='x', yl='y', one='1'):
        sq = Square(self.s, stroke_color=STROKE, stroke_width=4).move_to(self.P(.5, .5))
        labs = VGroup(scene.TM(f'${xl}$', 30, SOFT).next_to(self.P(1, 0), DOWN, buff=.12),
                      scene.TM(f'${yl}$', 30, SOFT).next_to(self.P(0, 1), LEFT, buff=.12),
                      scene.TM(f'${one}$', 24, SOFT).next_to(self.P(1, 0), DOWN, buff=.12).shift(LEFT * .4))
        return VGroup(sq, labs)

    def region(self, pts, color, op=.6, stroke=0):
        return Polygon(*[self.P(*p) for p in pts], stroke_color=color, stroke_width=stroke, fill_color=color, fill_opacity=op)
