"""Shared model for XSS337/338: a 3-ball box with 0..3 red equally likely, two red draws with replacement observed."""
from __future__ import annotations

from fractions import Fraction as F

PRIOR = [F(1, 4)] * 4
LIK = [F(k, 3) ** 2 for k in range(4)]
JOINT = [p * l for p, l in zip(PRIOR, LIK)]
POST = [j / sum(JOINT) for j in JOINT]
NEXT_RED = sum(p * F(k, 3) for k, p in enumerate(POST))


def urns_row(y=1.6):
    """Four small boxes with 0, 1, 2, 3 red balls among 3."""
    from manim import VGroup

    from common.visuals import urn
    return VGroup(*[urn('R' * k + 'B' * (3 - k), cols=3, r=.22) for k in range(4)]).arrange(buff=.35).move_to([0, y, 0])
