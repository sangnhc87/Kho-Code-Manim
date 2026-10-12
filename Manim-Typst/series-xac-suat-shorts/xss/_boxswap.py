"""Shared model for XSS403/404: draw from I (2R 1B); red → moved into II (1R 2B) then draw from II; blue → set aside, draw again from I."""
from __future__ import annotations

from fractions import Fraction as F

from common.theme import CORAL, CYAN

RED_FIRST = F(2, 3) * F(2, 4)      # II becomes 2R 2B
BLUE_FIRST = F(1, 3) * F(2, 2)     # I keeps 2R
RED_SECOND = RED_FIRST + BLUE_FIRST
BRANCHES = [('Đ', CORAL, '2/3', [('Đ', CORAL, '1/2', [])]), ('X', CYAN, '1/3', [('Đ', CORAL, '1', [])])]
