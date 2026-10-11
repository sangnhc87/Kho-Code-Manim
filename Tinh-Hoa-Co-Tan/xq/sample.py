"""Sinh thế cờ tàn hợp lệ theo vật chất cho trước, dùng để tìm thế dạy học."""
from __future__ import annotations

import random

from .board import BLACK, RED, Position

ADVISOR = [(3, 0), (5, 0), (4, 1), (3, 2), (5, 2)]
ELEPHANT = [(2, 0), (6, 0), (0, 2), (4, 2), (8, 2), (2, 4), (6, 4)]
PALACE = [(x, y) for x in range(3, 6) for y in range(3)]


def _mirror_y(points, side):
    return points if side == RED else [(x, 9 - y) for x, y in points]


def squares_for(u, side, pawn_crossed=True):
    if u == 'K':
        return _mirror_y(PALACE, side)
    if u == 'A':
        return _mirror_y(ADVISOR, side)
    if u == 'B':
        return _mirror_y(ELEPHANT, side)
    if u == 'P':
        pts = [(x, y) for x in range(9) for y in range(5, 10)]
        if not pawn_crossed:
            pts += [(x, y) for x in range(0, 9, 2) for y in (3, 4)]
        return _mirror_y(pts, side)
    return [(x, y) for x in range(9) for y in range(10)]


def random_position(red, black, turn=RED, rng=random, constraints=None, tries=5000):
    """red/black: chuỗi quân không kể Tướng, ví dụ 'NP', 'AB'.

    constraints: {'R': [ô...], 'a': [ô...]} giới hạn ô cho từng loại quân.
    """
    constraints = constraints or {}
    for _ in range(tries):
        cells = {}
        ok = True
        for side, mat in ((RED, 'K' + red), (BLACK, 'K' + black)):
            for u in mat:
                piece = u if side == RED else u.lower()
                pool = constraints.get(piece) or squares_for(u, side)
                free = [s for s in pool if s not in cells]
                if not free:
                    ok = False
                    break
                cells[rng.choice(free)] = piece
            if not ok:
                break
        if not ok:
            continue
        try:
            return Position.from_fen(Position(cells, turn).fen())
        except ValueError:
            continue
    raise RuntimeError(f'Không sinh được thế hợp lệ cho {red} vs {black}')


def canonical(fen):
    """Khoá chống trùng: thế và ảnh gương của nó coi là một."""
    pos = Position.from_fen(fen)
    return min(pos.fen(), pos.mirror().fen())
