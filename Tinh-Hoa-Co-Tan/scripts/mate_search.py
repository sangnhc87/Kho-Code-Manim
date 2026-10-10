#!/usr/bin/env python3
"""Exact AND-OR mate search for Xiangqi endgames (Red attacks, no promotion).

Proves "Red forces checkmate within k Red moves" by exhaustive search over all
Black replies. Stalemate/no legal move counts as a loss for the side to move.
Repetition and the 60-move rule are ignored, as in standard endgame tablebases.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.core import Board  # noqa: E402

EMPTY = '.'
FILES = 'abcdefghi'


def idx(x, y):
    return y * 9 + x


def xy(s):
    return s % 9, s // 9


def name(s):
    x, y = xy(s)
    return FILES[x] + str(y)


def in_palace(x, y, red):
    return 3 <= x <= 5 and (7 <= y <= 9 if red else 0 <= y <= 2)


def on_side(y, red):
    return y >= 5 if red else y <= 4


def _build_tables():
    horse, elephant, advisor, king = [], [], [], []
    for s in range(90):
        x, y = xy(s)
        h = []
        for dx, dy in ((1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < 9 and 0 <= ny < 10):
                continue
            leg = (x + dx // 2, y) if abs(dx) == 2 else (x, y + dy // 2)
            h.append((idx(nx, ny), idx(*leg)))
        horse.append(tuple(h))
        e, a, k = [], [], []
        for dx, dy in ((2, 2), (2, -2), (-2, 2), (-2, -2)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < 9 and 0 <= ny < 10:
                e.append((idx(nx, ny), idx(x + dx // 2, y + dy // 2)))
        elephant.append(tuple(e))
        for dx, dy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < 9 and 0 <= ny < 10:
                a.append(idx(nx, ny))
        advisor.append(tuple(a))
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < 9 and 0 <= ny < 10:
                k.append(idx(nx, ny))
        king.append(tuple(k))
    return tuple(horse), tuple(elephant), tuple(advisor), tuple(king)


HORSE, ELEPHANT, ADVISOR, KING = _build_tables()

# KNIGHT_ATTACK[t] = (attacker square, leg square adjacent to the attacker).
KNIGHT_ATTACK = tuple([] for _ in range(90))
for _s in range(90):
    for _dest, _leg in HORSE[_s]:
        KNIGHT_ATTACK[_dest].append((_s, _leg))
KNIGHT_ATTACK = tuple(tuple(v) for v in KNIGHT_ATTACK)


def is_red(c):
    return c.isupper()


def find_king(b, red):
    target = 'K' if red else 'k'
    try:
        return b.index(target)
    except ValueError:
        return -1


def facing(b):
    rk, bk = find_king(b, True), find_king(b, False)
    if rk < 0 or bk < 0:
        return False
    rx, ry = xy(rk)
    bx, by = xy(bk)
    if rx != bx:
        return False
    lo, hi = sorted((ry, by))
    return all(b[idx(rx, y)] == EMPTY for y in range(lo + 1, hi))


def attacked(b, t, by_red):
    """True if square t is attacked by a piece of side by_red (flying generals included)."""
    x, y = xy(t)
    for d, leg in KNIGHT_ATTACK[t]:
        if b[d] == ('N' if by_red else 'n') and b[leg] == EMPTY:
            return True
    for d, eye in ELEPHANT[t]:
        if b[d] == ('B' if by_red else 'b') and b[eye] == EMPTY and on_side(y, by_red):
            return True
    if in_palace(x, y, by_red):
        for d in ADVISOR[t]:
            if b[d] == ('A' if by_red else 'a'):
                return True
        for d in KING[t]:
            if b[d] == ('K' if by_red else 'k'):
                return True
    general = 'K' if by_red else 'k'
    for step in (9, -9):
        s = t + step
        while 0 <= s < 90 and b[s] == EMPTY:
            s += step
        if 0 <= s < 90 and b[s] == general:
            return True
    # Red pawns move toward y-1 and step sideways only after crossing the river (y <= 4).
    # Black pawns mirror this. The attacker stands behind the target (or beside it, if crossed).
    pawn = 'P' if by_red else 'p'
    behind = y + 1 if by_red else y - 1
    if 0 <= behind <= 9 and b[idx(x, behind)] == pawn:
        return True
    if on_side(y, not by_red):
        for dx in (-1, 1):
            if 0 <= x + dx < 9 and b[idx(x + dx, y)] == pawn:
                return True
    return False


def pseudo_moves(b, red):
    for s, c in enumerate(b):
        if c == EMPTY or c.isupper() != red:
            continue
        x, y = xy(s)
        t = c.upper()
        if t == 'K':
            dests = KING[s]
        elif t == 'A':
            dests = ADVISOR[s]
        elif t == 'B':
            dests = tuple(d for d, eye in ELEPHANT[s] if b[eye] == EMPTY and on_side(xy(d)[1], red))
        elif t == 'N':
            dests = tuple(d for d, leg in HORSE[s] if b[leg] == EMPTY)
        elif t == 'P':
            fwd = -1 if red else 1
            cand = [idx(x, y + fwd)] if 0 <= y + fwd <= 9 else []
            if on_side(y, not red):  # pawn has crossed the river
                cand += [idx(x + dx, y) for dx in (-1, 1) if 0 <= x + dx < 9]
            dests = cand
        else:
            raise ValueError(f'Unsupported piece {c}')
        for d in dests:
            dc = b[d]
            if dc != EMPTY and (dc.isupper() == red or dc.upper() == 'K'):
                continue
            if t in 'KA' and not in_palace(*xy(d), red):
                continue
            yield s, d


def apply(b, s, d):
    nb = list(b)
    nb[d] = nb[s]
    nb[s] = EMPTY
    return tuple(nb)


def legal_moves(b, red):
    out = []
    for s, d in pseudo_moves(b, red):
        nb = apply(b, s, d)
        k = find_king(nb, red)
        if k < 0 or attacked(nb, k, not red) or facing(nb):
            continue
        out.append((s, d, nb))
    return out


def red_in_check(b):
    return attacked(b, find_king(b, False), True)


def to_fen(b, red_to_move=True):
    rows = []
    for y in range(10):
        run, row = 0, ''
        for x in range(9):
            c = b[idx(x, y)]
            if c == EMPTY:
                run += 1
            else:
                if run:
                    row += str(run)
                    run = 0
                row += c
        if run:
            row += str(run)
        rows.append(row)
    return '/'.join(rows) + (' w' if red_to_move else ' b')


def from_fen(fen):
    Board.fen(fen)  # reuse core validation
    rows = fen.split()[0].split('/')
    b = [EMPTY] * 90
    for y, row in enumerate(rows):
        x = 0
        for ch in row:
            if ch.isdigit():
                x += int(ch)
            else:
                b[idx(x, y)] = ch
                x += 1
    return tuple(b)


class MateSearchAborted(Exception):
    """Raised internally when the node budget is exhausted."""


class MateSolver:
    """Memoised search: win_min[b] = smallest k proven winning, lose_max[b] = largest k proven not winning."""

    def __init__(self, node_cap=None):
        self.win_min = {}
        self.lose_max = {}
        self.dtm_memo = {}
        self.nodes = 0
        self.node_cap = node_cap

    def red_moves_ordered(self, b):
        moves = legal_moves(b, True)
        bk = find_king(b, False)
        scored = []
        for s, d, nb in moves:
            check = attacked(nb, bk, True)
            cap = b[d] != EMPTY
            scored.append((0 if check else (1 if cap else 2), s, d, nb))
        scored.sort(key=lambda t: t[0])
        return [(s, d, nb) for _, s, d, nb in scored]

    def mates_within(self, b, k):
        """Red to move: can Red force checkmate (or Black having no legal move) within k Red moves?"""
        if k <= 0:
            return False
        if b in self.win_min and k >= self.win_min[b]:
            return True
        if b in self.lose_max and k <= self.lose_max[b]:
            return False
        self.nodes += 1
        if self.node_cap is not None and self.nodes > self.node_cap:
            raise MateSearchAborted()
        for s, d, nb in self.red_moves_ordered(b):
            replies = legal_moves(nb, False)
            if not replies:
                self.win_min[b] = min(self.win_min.get(b, 1), 1)
                return True
            if k - 1 <= 0:
                continue
            # Black's most resistant replies: captures of Red pieces first (they often escape).
            replies.sort(key=lambda r: 0 if (nb[r[1]] != EMPTY) else 1)
            ok = True
            for _, _, bnb in replies:
                if not self.mates_within(bnb, k - 1):
                    ok = False
                    break
            if ok:
                self.win_min[b] = min(self.win_min.get(b, k), k)
                return True
        self.lose_max[b] = max(self.lose_max.get(b, 0), k)
        return False

    def dtm(self, b, red_to_move, cap=40):
        """Exact number of Red moves to mate under best play (Red fastest, Black slowest), or None if > cap."""
        key = (b, red_to_move)
        if key in self.dtm_memo:
            return self.dtm_memo[key]
        if red_to_move:
            result = None
            try:
                for k in range(1, cap + 1):
                    if self.mates_within(b, k):
                        result = k
                        break
            except MateSearchAborted:
                result = None
        else:
            replies = legal_moves(b, False)
            result = 0
            for _, _, nb in replies:
                v = self.dtm(nb, True, cap)
                if v is None:
                    result = None
                    break
                result = max(result, v)
        self.dtm_memo[key] = result
        return result


if __name__ == '__main__':
    print(__doc__)
