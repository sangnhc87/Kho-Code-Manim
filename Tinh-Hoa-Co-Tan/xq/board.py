"""Luật cờ tướng đầy đủ, dùng đúng hệ toạ độ của chessdb.cn / Pikafish.

Toạ độ: cột a..i từ trái sang phải (nhìn từ phía Đỏ), hàng 0..9 từ dưới lên.
Hàng 0 là hàng đáy của Đỏ, hàng 9 là hàng đáy của Đen. Nước đi viết kiểu UCI
"h2e2". FEN liệt kê từ hàng 9 xuống hàng 0, chữ hoa là Đỏ, chữ thường là Đen.
"""
from __future__ import annotations

RED, BLACK = 'w', 'b'
FILES = 'abcdefghi'

KNIGHT_STEPS = [((1, 2), (0, 1)), ((-1, 2), (0, 1)), ((1, -2), (0, -1)), ((-1, -2), (0, -1)),
                ((2, 1), (1, 0)), ((2, -1), (1, 0)), ((-2, 1), (-1, 0)), ((-2, -1), (-1, 0))]
ORTHO = [(1, 0), (-1, 0), (0, 1), (0, -1)]
DIAG = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
# Bảng chuẩn hoá chữ cái quân: một số nguồn dùng H cho Mã và E cho Tượng.
ALIASES = {'h': 'n', 'e': 'b'}


def side_of(piece):
    return RED if piece.isupper() else BLACK


def other(side):
    return BLACK if side == RED else RED


def sq_name(sq):
    return FILES[sq[0]] + str(sq[1])


def parse_sq(name):
    if len(name) != 2 or name[0] not in FILES or not name[1].isdigit():
        raise ValueError(f'Ô không hợp lệ: {name!r}')
    return FILES.index(name[0]), int(name[1])


def in_palace(sq, side):
    x, y = sq
    return 3 <= x <= 5 and (0 <= y <= 2 if side == RED else 7 <= y <= 9)


def own_half(sq, side):
    return sq[1] <= 4 if side == RED else sq[1] >= 5


def on_board(sq):
    return 0 <= sq[0] <= 8 and 0 <= sq[1] <= 9


class Position:
    __slots__ = ('cells', 'turn')

    def __init__(self, cells, turn=RED):
        self.cells = dict(cells)
        self.turn = turn

    # ---------- FEN ----------
    @classmethod
    def from_fen(cls, fen):
        parts = fen.split()
        rows = parts[0].split('/')
        if len(rows) != 10:
            raise ValueError('FEN cờ tướng phải có 10 hàng')
        cells = {}
        for i, row in enumerate(rows):
            y = 9 - i
            x = 0
            for ch in row:
                if ch.isdigit():
                    x += int(ch)
                    continue
                low = ALIASES.get(ch.lower(), ch.lower())
                if low not in 'kabnrcp':
                    raise ValueError(f'Ký tự quân lạ: {ch}')
                if x > 8:
                    raise ValueError('Hàng FEN quá 9 cột')
                cells[(x, y)] = low.upper() if ch.isupper() else low
                x += 1
            if x != 9:
                raise ValueError(f'Hàng FEN {i} có {x} cột')
        turn = BLACK if len(parts) > 1 and parts[1] == 'b' else RED
        pos = cls(cells, turn)
        pos.validate()
        return pos

    def fen(self):
        rows = []
        for y in range(9, -1, -1):
            row, gap = '', 0
            for x in range(9):
                p = self.cells.get((x, y))
                if p:
                    if gap:
                        row += str(gap)
                        gap = 0
                    row += p
                else:
                    gap += 1
            rows.append(row + (str(gap) if gap else ''))
        return '/'.join(rows) + ' ' + self.turn

    def copy(self):
        return Position(self.cells, self.turn)

    def validate(self):
        kings = [p for p in self.cells.values() if p in 'Kk']
        if sorted(kings) != ['K', 'k']:
            raise ValueError('Mỗi bên phải có đúng một Tướng')
        limits = {'k': 1, 'a': 2, 'b': 2, 'n': 2, 'r': 2, 'c': 2, 'p': 5}
        for p, n in limits.items():
            for q in (p, p.upper()):
                if sum(v == q for v in self.cells.values()) > n:
                    raise ValueError(f'Thừa quân {q}')
        for sq, p in self.cells.items():
            s = side_of(p)
            u = p.upper()
            if u in 'KA' and not in_palace(sq, s):
                raise ValueError(f'{p} ngoài cung tại {sq_name(sq)}')
            if u == 'A' and (sq[0] + sq[1] + (0 if s == RED else 1)) % 2 == 0:
                raise ValueError(f'Sĩ đứng sai điểm {sq_name(sq)}')
            if u == 'B':
                legal = {(2, 0), (6, 0), (0, 2), (4, 2), (8, 2), (2, 4), (6, 4)}
                if s == BLACK:
                    legal = {(x, 9 - y) for x, y in legal}
                if sq not in legal:
                    raise ValueError(f'Tượng đứng sai điểm {sq_name(sq)}')
            if u == 'P':
                y = sq[1] if s == RED else 9 - sq[1]
                if y < 3 or (y < 5 and sq[0] % 2 == 1):
                    raise ValueError(f'Tốt đứng sai điểm {sq_name(sq)}')
        if self.kings_facing():
            raise ValueError('Hai Tướng đối mặt')
        if self.in_check(other(self.turn)):
            raise ValueError('Bên vừa đi xong đang bị chiếu')

    # ---------- tấn công / chiếu ----------
    def king_sq(self, side):
        target = 'K' if side == RED else 'k'
        for sq, p in self.cells.items():
            if p == target:
                return sq
        return None

    def kings_facing(self):
        a, b = self.king_sq(RED), self.king_sq(BLACK)
        if not a or not b or a[0] != b[0]:
            return False
        return not any((a[0], y) in self.cells for y in range(a[1] + 1, b[1]))

    def count_between(self, a, b):
        if a[0] == b[0]:
            lo, hi = sorted((a[1], b[1]))
            return sum((a[0], y) in self.cells for y in range(lo + 1, hi))
        if a[1] == b[1]:
            lo, hi = sorted((a[0], b[0]))
            return sum((x, a[1]) in self.cells for x in range(lo + 1, hi))
        return None

    def attacks(self, src, dst):
        """Quân ở src có khống chế (ăn được) ô dst hay không (không xét tự chiếu)."""
        p = self.cells.get(src)
        if not p or src == dst:
            return False
        s, u = side_of(p), p.upper()
        dx, dy = dst[0] - src[0], dst[1] - src[1]
        if u == 'R':
            return self.count_between(src, dst) == 0
        if u == 'C':
            n = self.count_between(src, dst)
            return n is not None and n == (1 if dst in self.cells else 0)
        if u == 'N':
            for (sx, sy), (lx, ly) in KNIGHT_STEPS:
                if (dx, dy) == (sx, sy):
                    return (src[0] + lx, src[1] + ly) not in self.cells
            return False
        if u == 'P':
            fwd = 1 if s == RED else -1
            if dx == 0 and dy == fwd:
                return True
            return dy == 0 and abs(dx) == 1 and not own_half(src, s)
        if u == 'K':
            return abs(dx) + abs(dy) == 1 and in_palace(dst, s)
        if u == 'A':
            return abs(dx) == 1 and abs(dy) == 1 and in_palace(dst, s)
        if u == 'B':
            return (abs(dx) == 2 and abs(dy) == 2 and own_half(dst, s)
                    and (src[0] + dx // 2, src[1] + dy // 2) not in self.cells)
        return False

    def in_check_slow(self, side):
        k = self.king_sq(side)
        if k is None:
            return True
        if self.kings_facing():
            return True
        return any(side_of(p) != side and self.attacks(sq, k) for sq, p in self.cells.items())

    def in_check(self, side):
        """Kiểm tra chiếu nhanh: dò từ ô Tướng ra các hướng thay vì xét mọi quân."""
        cells = self.cells
        k = self.king_sq(side)
        if k is None:
            return True
        kx, ky = k
        red = side == RED
        R, C, N, P, K = ('r', 'c', 'n', 'p', 'k') if red else ('R', 'C', 'N', 'P', 'K')
        for dx, dy in ORTHO:
            x, y, screen = kx + dx, ky + dy, False
            while 0 <= x <= 8 and 0 <= y <= 9:
                q = cells.get((x, y))
                if q:
                    if not screen:
                        if q == R or (q == K and dx == 0):
                            return True
                        screen = True
                    else:
                        if q == C:
                            return True
                        break
                x, y = x + dx, y + dy
        for (sx, sy), (lx, ly) in KNIGHT_STEPS:
            src = (kx - sx, ky - sy)
            if cells.get(src) == N and (src[0] + lx, src[1] + ly) not in cells:
                return True
        fwd = 1 if not red else -1  # hướng tiến của Tốt đối phương
        if cells.get((kx, ky - fwd)) == P:
            return True
        for dx in (-1, 1):
            q = (kx + dx, ky)
            if cells.get(q) == P and not own_half(q, BLACK if red else RED):
                return True
        return False

    def checkers(self, side):
        """Danh sách ô các quân đang chiếu Tướng của side."""
        k = self.king_sq(side)
        return [sq for sq, p in self.cells.items() if side_of(p) != side and self.attacks(sq, k)]

    # ---------- sinh nước ----------
    def pseudo_targets(self, src):
        p = self.cells[src]
        s, u = side_of(p), p.upper()
        x, y = src
        out = []
        if u in 'RC':
            for dx, dy in ORTHO:
                nx, ny, jumped = x + dx, y + dy, False
                while on_board((nx, ny)):
                    t = self.cells.get((nx, ny))
                    if u == 'R':
                        if t is None:
                            out.append((nx, ny))
                        else:
                            if side_of(t) != s:
                                out.append((nx, ny))
                            break
                    else:
                        if not jumped:
                            if t is None:
                                out.append((nx, ny))
                            else:
                                jumped = True
                        elif t is not None:
                            if side_of(t) != s:
                                out.append((nx, ny))
                            break
                    nx, ny = nx + dx, ny + dy
        elif u == 'N':
            for (sx, sy), (lx, ly) in KNIGHT_STEPS:
                d = (x + sx, y + sy)
                if on_board(d) and (x + lx, y + ly) not in self.cells:
                    out.append(d)
        else:
            if u == 'K':
                cand = [(x + dx, y + dy) for dx, dy in ORTHO]
            elif u == 'A':
                cand = [(x + dx, y + dy) for dx, dy in DIAG]
            elif u == 'B':
                cand = [(x + 2 * dx, y + 2 * dy) for dx, dy in DIAG]
            else:
                fwd = 1 if s == RED else -1
                cand = [(x, y + fwd)]
                if not own_half(src, s):
                    cand += [(x - 1, y), (x + 1, y)]
            out = [d for d in cand if on_board(d) and self.attacks(src, d)]
        return [d for d in out if d not in self.cells or side_of(self.cells[d]) != s]

    def legal_moves(self):
        moves = []
        cells = self.cells
        for src, p in list(cells.items()):
            if side_of(p) != self.turn:
                continue
            for dst in self.pseudo_targets(src):
                victim = cells.get(dst)
                if victim and victim.upper() == 'K':
                    continue
                # đi thử tại chỗ rồi hoàn lại (nhanh hơn tạo thế mới)
                cells[dst] = cells.pop(src)
                ok = not self.in_check(self.turn)
                cells[src] = cells.pop(dst)
                if victim:
                    cells[dst] = victim
                if ok:
                    moves.append(sq_name(src) + sq_name(dst))
        return sorted(moves)

    def _apply(self, src, dst):
        nxt = Position(self.cells, other(self.turn))
        nxt.cells[dst] = nxt.cells.pop(src)
        return nxt

    def play(self, move):
        """Trả về thế mới sau nước UCI; báo lỗi nếu nước không hợp lệ."""
        if move not in self.legal_moves():
            raise ValueError(f'Nước {move} không hợp lệ trong thế {self.fen()}')
        return self._apply(parse_sq(move[:2]), parse_sq(move[2:]))

    def is_mate(self):
        """Hết nước đi (bị chiếu bí hoặc bị vây hết nước): trong cờ tướng đều là thua."""
        return not self.legal_moves()

    def material(self, side):
        return ''.join(sorted((p.upper() for p in self.cells.values() if side_of(p) == side),
                              key='KRNCABP'.index))

    def mirror(self):
        return Position({(8 - x, y): p for (x, y), p in self.cells.items()}, self.turn)

    def flip_turn(self):
        return Position(self.cells, other(self.turn))
