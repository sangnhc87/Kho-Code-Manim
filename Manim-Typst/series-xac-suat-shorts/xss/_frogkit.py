"""Shared props for the frog / walk Shorts (XSS281+): a row of lily pads and a frog marker."""
from __future__ import annotations

from manim import Circle, Dot, Ellipse, VGroup

from common.theme import GREEN, SOFT

PAD = '#2F7D4F'


def pads(labels, y=1.6, gap=1.15, r=.42, bad=()):
    """Row of lily pads with numeric labels under them; ``bad`` pads are drawn dark (broken)."""
    g = VGroup()
    n = len(labels)
    for i, lab in enumerate(labels):
        x = (i - (n - 1) / 2) * gap
        leaf = Ellipse(width=2 * r, height=1.2 * r, fill_color='#334155' if lab in bad else PAD, fill_opacity=1,
                       stroke_color=SOFT, stroke_width=2).move_to([x, y, 0])
        g.add(leaf)
    return g


def frog(r=.2):
    body = Circle(radius=r, fill_color=GREEN, fill_opacity=1, stroke_color='#0B1220', stroke_width=3)
    eyes = VGroup(*[Dot(radius=r * .22, color='#0B1220').move_to(body.get_center() + [s * r * .45, r * .45, 0]) for s in (-1, 1)])
    return VGroup(body, eyes)
