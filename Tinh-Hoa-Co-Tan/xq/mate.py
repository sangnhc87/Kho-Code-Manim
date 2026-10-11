"""Chứng minh sát cục bằng tìm kiếm vét cạn: bên tấn công chiếu liên tục, xét MỌI nước chống đỡ.

Trong cờ tướng, bên hết nước đi là thua, nên 'chiếu bí' = sau nước chiếu đối phương không còn
nước hợp lệ. Kết quả là một chứng minh chính xác (không phải đánh giá của engine).
"""
from __future__ import annotations

from .board import Position, parse_sq, side_of


class Budget(Exception):
    pass


class Prover:
    def __init__(self, max_nodes=400_000):
        self.max_nodes = max_nodes
        self.nodes = 0
        self.cache = {}
        self.lm = {}

    def legal(self, pos):
        key = pos.fen()
        if key not in self.lm:
            self.nodes += 1
            if self.nodes > self.max_nodes:
                raise Budget()
            self.lm[key] = pos.legal_moves()
        return self.lm[key]

    def checks(self, pos):
        out = []
        for m in self.legal(pos):
            nxt = pos.play(m)
            if nxt.in_check(nxt.turn):
                out.append((m, nxt))
        return out

    def mates_in(self, pos, n):
        """Các nước chiếu đầu tiên dẫn tới bí trong đúng tối đa n nước của bên tấn công."""
        key = (pos.fen(), n)
        if key in self.cache:
            return self.cache[key]
        good = []
        for m, nxt in self.checks(pos):
            replies = self.legal(nxt)
            if not replies:
                good.append(m)
                continue
            if n == 1:
                continue
            if all(self.mates_in(nxt.play(r), n - 1) for r in replies):
                good.append(m)
        self.cache[key] = good
        return good

    def solve(self, fen, max_n=9):
        pos = Position.from_fen(fen)
        for n in range(1, max_n + 1):
            first = self.mates_in(pos, n)
            if first:
                return n, first
        return None, []

    def depth(self, pos, cap):
        """Số nước chiếu ít nhất để bí từ pos (bên tấn công đi)."""
        for n in range(1, cap + 1):
            if self.mates_in(pos, n):
                return n
        return None

    def main_line(self, fen, n, first):
        """Biến chính: bên tấn công đi nước bí nhanh nhất; bên phòng thủ chống lâu nhất,
        ưu tiên nước ăn quân (để lộ rõ đòn thí quân)."""
        pos = Position.from_fen(fen)
        line = []
        k = n
        move = first
        while True:
            nxt = pos.play(move)
            sac = sacrifice(pos, move)
            line.append({'move': move, 'side': pos.turn, 'check': True, 'sacrifice': sac,
                         'capture': pos.cells.get(parse_sq(move[2:]))})
            replies = self.legal(nxt)
            if not replies:
                break
            k -= 1
            scored = []
            for r in replies:
                after = nxt.play(r)
                d = self.depth(after, k)
                scored.append((d or 0, 1 if nxt.cells.get(parse_sq(r[2:])) else 0, r, after))
            d, cap, r, after = max(scored, key=lambda t: (t[0], t[1]))
            line.append({'move': r, 'side': nxt.turn, 'forced': len(replies) == 1,
                         'capture': nxt.cells.get(parse_sq(r[2:])), 'n_replies': len(replies)})
            pos = after
            move = self.mates_in(pos, k)[0]
        return line


def sacrifice(pos, move):
    """Nước đưa quân tới ô mà đối phương ăn được (không tính Tướng): đòn thí quân."""
    nxt = pos.play(move)
    dst = parse_sq(move[2:])
    piece = nxt.cells[dst]
    if piece.upper() == 'K':
        return None
    for m in nxt.legal_moves():
        if parse_sq(m[2:]) == dst:
            return piece.upper()
    return None
