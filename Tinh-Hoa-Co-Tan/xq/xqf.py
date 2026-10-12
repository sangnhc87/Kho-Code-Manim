"""Đọc kỳ phổ XQF (Tượng Kỳ Vu Sư) phiên bản 10, không mã hoá: thế khởi đầu + cây nước đi.

Header 1024 byte: [16:48] vị trí 32 quân (x*10+y, 0xFF = không có), thứ tự mỗi bên
Xe Mã Tượng Sĩ Tướng Sĩ Tượng Mã Xe Pháo Pháo Binh x5 (16 quân đầu là Đỏ); [50] bên đi trước; [51] kết quả.
Thân: các nút [xyFrom+0x18, xyTo+0x20, cờ, 0] + dword độ dài lời bình (luôn có) + lời bình; duyệt theo chiều sâu:
nút, rồi nước kế (cờ & 0xF0), rồi biến thay thế (cờ & 0x0F). Lời bình KHÔNG được đọc ra (bản quyền).
"""
from __future__ import annotations

import struct
import sys

from .board import BLACK, FILES, RED, Position

ORDER = 'RNBAKABNRCCPPPPP'


def sq(v):
    return (v // 10, v % 10)


def read(path):
    b = open(path, 'rb').read()
    if b[:2] != b'XQ' or b[2] > 10 or b[3] != 0:
        raise ValueError(f'{path}: chỉ hỗ trợ XQF v≤10 không mã hoá (v={b[2]}, key={b[3]})')
    cells = {}
    for i in range(32):
        v = b[16 + i]
        if v == 0xFF:
            continue
        piece = ORDER[i % 16]
        cells[sq(v)] = piece if i < 16 else piece.lower()
    turn = RED if b[50] == 0 else BLACK
    start = Position(cells, turn)
    pos = [1024]

    def node():
        i = pos[0]
        xf, xt, flag = b[i] - 0x18, b[i + 1] - 0x20, b[i + 2]
        n = struct.unpack_from('<I', b, i + 4)[0]
        pos[0] = i + 8 + n          # luôn có dword độ dài lời bình (có thể 0); không đọc nội dung
        out = {'f': xf, 't': xt, 'next': None, 'alt': None}
        if flag & 0xF0:
            out['next'] = node()
        if flag & 0x0F:
            out['alt'] = node()
        return out

    sys.setrecursionlimit(20000)
    root = node()
    return start, root, b[51]


def uci(xf, xt):
    (x1, y1), (x2, y2) = sq(xf), sq(xt)
    return f'{FILES[x1]}{y1}{FILES[x2]}{y2}'


def to_tree(root, start):
    """Cây {'c': [{m, ply, c}]} chuẩn của dự án; nước không hợp lệ cắt nhánh và đếm vào errors."""
    errors = []

    def build(nd, pos, ply):
        """nd = nút nước đầu tiên của danh sách anh em (nd, nd.alt, ...)."""
        kids = []
        while nd is not None:
            m = uci(nd['f'], nd['t'])
            if m not in pos.legal_moves():
                errors.append((ply + 1, m))
            else:
                child = {'m': m, 'ply': ply + 1}
                sub = build(nd['next'], pos.play(m), ply + 1)
                if sub:
                    child['c'] = sub
                kids.append(child)
            nd = nd['alt']
        return kids

    # nút gốc là nút giả (không có nước); các nước thật bắt đầu từ root['next']
    kids = build(root['next'], start, 0)
    return {'c': kids} if kids else {}, errors
