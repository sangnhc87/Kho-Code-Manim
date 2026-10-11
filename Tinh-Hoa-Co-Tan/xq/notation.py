"""Ký pháp cờ tướng Việt Nam: "Mã 2 tiến 3", "Xe trước bình 4", "Tốt 5 tiến 1".

- Cột đánh số 1..9 từ phải sang trái theo hướng nhìn của bên đi quân:
  Đỏ: cột i = 1 ... cột a = 9; Đen: cột a = 1 ... cột i = 9.
- Quân đi thẳng (Xe, Pháo, Tốt, Tướng): tiến/thoái kèm số bước, bình kèm cột đích.
- Quân đi chéo (Mã, Sĩ, Tượng): số sau tiến/thoái là cột đích.
- Hai quân cùng loại trên một cột: gọi "trước"/"sau" thay cho số cột.
"""
from __future__ import annotations

from .board import RED, parse_sq, side_of

NAMES = {'K': 'Tướng', 'A': 'Sĩ', 'B': 'Tượng', 'N': 'Mã', 'R': 'Xe', 'C': 'Pháo'}
SHORT = {'K': 'Tg', 'A': 'S', 'B': 'T', 'N': 'M', 'R': 'X', 'C': 'P'}
# Tên quân khi đọc thành lời và khi ghi trên bảng nước đi.
FULL_NAMES = {'K': 'Tướng', 'A': 'Sĩ', 'B': 'Tượng', 'N': 'Mã', 'R': 'Xe', 'C': 'Pháo', 'P': 'Tốt'}
DIAGONAL = 'NAB'


def piece_name(piece):
    u = piece.upper()
    if u == 'P':
        return 'Binh' if piece.isupper() else 'Tốt'
    return NAMES[u]


def file_no(x, side):
    return 9 - x if side == RED else x + 1


def _forward(dy, side):
    return dy if side == RED else -dy


def _prefix(pos, src, piece):
    side = side_of(piece)
    same = sorted((sq for sq, p in pos.cells.items() if p == piece and sq[0] == src[0]),
                  key=lambda s: s[1], reverse=(side == RED))
    name = piece_name(piece)
    if len(same) < 2:
        return f'{name} {file_no(src[0], side)}'
    idx = same.index(src)
    if len(same) == 2:
        return f'{name} {"trước" if idx == 0 else "sau"}'
    if len(same) == 3:
        return f'{name} {("trước", "giữa", "sau")[idx]}'
    return f'{name} {("một", "hai", "ba", "bốn", "năm")[idx]}'


def vn_move(pos, move):
    """Ký pháp Việt của nước UCI trong thế pos (trước khi đi)."""
    src, dst = parse_sq(move[:2]), parse_sq(move[2:])
    piece = pos.cells[src]
    side = side_of(piece)
    u = piece.upper()
    head = _prefix(pos, src, piece)
    dy = _forward(dst[1] - src[1], side)
    if dy == 0:
        return f'{head} bình {file_no(dst[0], side)}'
    verb = 'tiến' if dy > 0 else 'thoái'
    num = file_no(dst[0], side) if u in DIAGONAL else abs(dy)
    return f'{head} {verb} {num}'


def short_move(pos, move):
    """Ký hiệu rút gọn cho bảng nước đi: M2.3, X1-4, P8/1."""
    text = vn_move(pos, move)
    parts = text.split()
    name, ident, verb, num = parts[0], parts[1], parts[2], parts[3]
    abbr = {'Tướng': 'Tg', 'Sĩ': 'S', 'Tượng': 'T', 'Mã': 'M', 'Xe': 'X', 'Pháo': 'P',
            'Binh': 'B', 'Tốt': 'B'}[name]
    ident = {'trước': 't', 'sau': 's', 'giữa': 'g'}.get(ident, ident)
    sym = {'tiến': '.', 'thoái': '/', 'bình': '-'}[verb]
    return f'{abbr}{ident}{sym}{num}'


def spoken(text):
    """Chuỗi để TTS đọc tự nhiên (giữ nguyên số, bỏ ký hiệu)."""
    return text.replace('—', ',').replace('…', '.')
