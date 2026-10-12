"""Shared model for XSS361/362: die gives k, then k balls drawn from 4 red + 3 blue; event = all k red."""
from __future__ import annotations

from fractions import Fraction as F
from math import comb

from common.theme import CORAL, CYAN

ALLRED = {k: F(comb(4, k), comb(7, k)) for k in range(1, 7)}
TOTAL = sum(F(1, 6) * ALLRED[k] for k in range(1, 7))
LEAF = {1: '4/7', 2: '2/7', 3: '4/35', 4: '1/35', 5: '0', 6: '0'}
BRANCHES = [(str(k), CYAN, '1/6', [('Đ', CORAL, LEAF[k], [])]) for k in range(1, 7)]
