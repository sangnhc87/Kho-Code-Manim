"""Shared helpers for the multi-box ball Shorts (XSS201+): two or three labelled urns side by side."""
from __future__ import annotations

from manim import VGroup

from common.kit import tx
from common.theme import SOFT
from common.visuals import urn


def urn_row(specs, y=1.7, r=.26, buff=.6, label_size=24):
    """specs = [(colors, label, color), ...] → VGroup of (urn, label); fits the 7.4-wide stage."""
    g = VGroup()
    for colors, label, color in specs:
        u = urn(colors, cols=3, r=r)
        g.add(VGroup(u, tx(label, label_size, color or SOFT).next_to(u, [0, -1, 0], buff=.1)))
    g.arrange(buff=buff)
    if g.width > 7.4:
        g.scale_to_fit_width(7.4)
    return g.move_to([0, y, 0])
