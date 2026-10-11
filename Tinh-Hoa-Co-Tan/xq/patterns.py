"""Nhận diện vài thế sát kinh điển ở thế bí cuối cùng (chỉ những định nghĩa chắc chắn).

- Trùng Pháo (重炮): Pháo chiếu, ngòi là một Pháo khác cùng bên.
- Mã hậu Pháo (马后炮): Pháo chiếu, ngòi là Mã cùng bên.
- Muộn cung (闷宫): Pháo chiếu, các ô thoát của Tướng bị chính hai Sĩ của nó chặn.
- Bạch diện tướng (白脸将): Tướng bên thắng khống chế ô thoát nhờ luật lộ mặt tướng.
"""
from __future__ import annotations

from .analyze import mate_anatomy
from .board import parse_sq, side_of


def screen_between(pos, a, b):
    if a[0] == b[0]:
        lo, hi = sorted((a[1], b[1]))
        squares = [(a[0], y) for y in range(lo + 1, hi)]
    else:
        lo, hi = sorted((a[0], b[0]))
        squares = [(x, a[1]) for x in range(lo + 1, hi)]
    pieces = [(s, pos.cells[s]) for s in squares if s in pos.cells]
    return pieces[0] if len(pieces) == 1 else None


def mate_patterns(pos):
    """pos: thế đã bí (bên đi là bên thua). Trả về danh sách tên thế sát nhận diện được."""
    if not pos.is_mate():
        return []
    loser = pos.turn
    an = mate_anatomy(pos)
    king = parse_sq(an['king'])
    names = []
    for c in an['checkers']:
        sq_name_, piece = c.split(':')
        if piece.upper() != 'C':
            continue
        scr = screen_between(pos, parse_sq(sq_name_), king)
        if not scr:
            continue
        sp = scr[1]
        if side_of(sp) != loser and sp.upper() == 'C':
            names.append('Trùng Pháo')
        elif side_of(sp) != loser and sp.upper() == 'N':
            names.append('Mã hậu Pháo')
        own_adv = [e for e in an['escapes'] if e.get('blocked_by_own', '').upper() == 'A']
        if len(own_adv) >= 2 and all('blocked_by_own' in e for e in an['escapes']):
            names.append('Muộn cung')
    if any(any(g.endswith(':mặt') for g in e.get('guards', [])) for e in an['escapes']):
        names.append('Bạch diện tướng')
    return list(dict.fromkeys(names))
