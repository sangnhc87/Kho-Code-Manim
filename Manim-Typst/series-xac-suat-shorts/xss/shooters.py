"""Shared scene base for XSS041 – XSS043 (two independent shooters)."""
from __future__ import annotations

import sys
from pathlib import Path

from manim import DOWN, LEFT, UP, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import ShortScene  # noqa: E402
from common.theme import CORAL, CYAN  # noqa: E402
from common.visuals import unit_square  # noqa: E402


class ShooterSquare(ShortScene):
    """Shared hook: the unit square of two independent shooters (p = 0,8; q = 0,7)."""

    def hook_visual(self, t0):
        self.board_top = -1.1
        self.sq = unit_square(.8, .7, 3.7, (.2, 1.35))
        self.labels = VGroup(
            self.TM('$P(A) = "0,8"$', 24, CYAN).next_to(self.sq[0], DOWN, buff=.12).align_to(self.sq[0], LEFT),
            self.TM('$P(B) = "0,7"$', 24, CORAL).rotate(1.5708).next_to(self.sq[0], LEFT, buff=.12)
            .align_to(self.sq[0], UP))
        self.wait_until(.55, t0)
        self.play(FadeIn(self.sq), FadeIn(self.labels), run_time=self.rt(.15))
