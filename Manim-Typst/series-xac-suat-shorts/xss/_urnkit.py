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


def transfer_arrow(src, dst, label='', color=None):
    """Curved arrow from urn group src to urn group dst with an optional label above it."""
    from manim import CurvedArrow, VGroup as VG

    from common.theme import GOLD
    a = CurvedArrow(src[0].get_top() + [0, .1, 0], dst[0].get_top() + [0, .1, 0], angle=-1.0, color=color or GOLD,
                    stroke_width=5)
    g = VG(a)
    if label:
        g.add(tx(label, 22, color or GOLD).next_to(a, [0, 1, 0], buff=.05))
    return g
