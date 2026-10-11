"""Đọc kỳ phổ định dạng DhtmlXQ (Đông Bình, .dpxq) thành FEN + danh sách nước UCI.

binit: 64 chữ số = 32 quân x 2 chữ số (cột x 0-8 từ trái, hàng y 0-9 từ trên/phía Đen),
"99" = quân không có. Thứ tự quân mỗi bên: Xe Mã Tượng Sĩ Tướng Sĩ Tượng Mã Xe Pháo Pháo
Binh x5; 16 quân đầu là Đỏ. movelist: nhóm 4 chữ số x1y1x2y2.
"""
from __future__ import annotations

import re

from .board import BLACK, RED, Position, sq_name

ORDER = 'RNBAKABNRCCPPPPP'
TAG = re.compile(r'\[DhtmlXQ_(\w+)\](.*?)\[/DhtmlXQ_\w+\]', re.S)


def tags(text):
    return {k: v.strip() for k, v in TAG.findall(text.lstrip('﻿'))}


def _sq(x, y):
    return (int(x), 9 - int(y))


def board_from_binit(binit, turn=RED):
    if len(binit) != 64:
        raise ValueError('binit phải có 64 chữ số')
    cells = {}
    for i in range(32):
        xy = binit[2 * i:2 * i + 2]
        if xy == '99':
            continue
        piece = ORDER[i % 16]
        cells[_sq(xy[0], xy[1])] = piece if i < 16 else piece.lower()
    return Position(cells, turn)


def moves_from_list(movelist):
    out = []
    for i in range(0, len(movelist) - 3, 4):
        g = movelist[i:i + 4]
        out.append(sq_name(_sq(g[0], g[1])) + sq_name(_sq(g[2], g[3])))
    return out


def parse(text):
    """Trả về dict: fen (thế đầu), moves (biến chính của kỳ phổ), result, title, red, black, event..."""
    t = tags(text)
    binit = t.get('binit') or ''
    moves = moves_from_list(t.get('movelist', ''))
    pos = board_from_binit(binit, RED)
    # Bên đi trước: thử Đỏ, nếu nước đầu không hợp lệ thì là Đen.
    if moves and moves[0] not in pos.legal_moves():
        pos = Position(pos.cells, BLACK)
    pos = Position.from_fen(pos.fen())
    return {
        'fen': pos.fen(),
        'moves': moves,
        'result': t.get('result', ''),
        'title': t.get('title', ''),
        'red': t.get('red', ''),
        'black': t.get('black', ''),
        'event': t.get('event', ''),
        'date': t.get('date', ''),
        'type': t.get('type', ''),
    }


def replay(fen, moves):
    """Các thế dọc theo kỳ phổ; dừng ở nước không hợp lệ đầu tiên."""
    pos = Position.from_fen(fen)
    out = [pos]
    for m in moves:
        if m not in pos.legal_moves():
            break
        pos = pos.play(m)
        out.append(pos)
    return out
