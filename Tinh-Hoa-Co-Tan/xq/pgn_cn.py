"""Đọc kỳ phổ PGN ký pháp Hán (GBK) có biến lồng nhau thành cây nước đi UCI.

Ví dụ nước: "炮二平五", "马８进７", "前车进一", "后炮平四". Đỏ ghi số Hán, Đen ghi số toàn rộng.
Biến "( ... )" thay thế nước đi ngay trước nó (ngữ nghĩa PGN chuẩn). Nước không đọc được
hoặc không hợp lệ sẽ cắt nhánh tại đó và được ghi vào danh sách lỗi.
"""
from __future__ import annotations

import re

from .board import BLACK, RED, Position, parse_sq, sq_name

PIECE = {'车': 'R', '車': 'R', '马': 'N', '馬': 'N', '傌': 'N', '炮': 'C', '砲': 'C', '包': 'C',
         '相': 'B', '象': 'B', '仕': 'A', '士': 'A', '帅': 'K', '帥': 'K', '将': 'K', '將': 'K',
         '兵': 'P', '卒': 'P'}
NUM = {c: i + 1 for i, c in enumerate('一二三四五六七八九')}
NUM.update({c: i + 1 for i, c in enumerate('１２３４５６７８９')})
NUM.update({c: i + 1 for i, c in enumerate('123456789')})
PREFIX = {'前': 'front', '后': 'back', '後': 'back', '中': 'mid', '二': 2, '三': 3, '四': 4, '五': 5}
DIRS = {'进': 1, '進': 1, '退': -1, '平': 0}
MOVE_RE = re.compile(r'([前后後中二三四五]?)([车車马馬傌炮砲包相象仕士帅帥将將兵卒]?)([一二三四五六七八九１-９1-9]?)([进進退平])([一二三四五六七八九１-９1-9]?)')


def decode(path):
    return open(path, 'rb').read().decode('gb18030', 'replace')


def resolve(pos, text):
    """Nước ký pháp Hán -> UCI trong thế pos, hoặc None nếu không đọc/không hợp lệ."""
    text = text.replace(' ', '').replace('　', '')
    m = MOVE_RE.fullmatch(text)
    if not m:
        return None
    pre, pch, f1, dch, n = m.groups()
    if not n or dch not in DIRS:
        return None
    side = pos.turn
    sign = 1 if side == RED else -1
    legal = set(pos.legal_moves())

    def to_x(num):
        return 9 - num if side == RED else num - 1

    if pre:
        # Ký hiệu "前车": nhận quân từ chữ sau tiền tố
        ptype = PIECE.get(pch)
        if not ptype:
            return None
        mine = [(sq, p) for sq, p in pos.cells.items()
                if p.upper() == ptype and (p.isupper() == (side == RED))]
        by_file = {}
        for sq, _ in mine:
            by_file.setdefault(sq[0], []).append(sq)
        cands = []
        for x, sqs in by_file.items():
            if len(sqs) < 2:
                continue
            sqs.sort(key=lambda s: s[1], reverse=(side == RED))   # [0] = tiến xa nhất
            kind = PREFIX[pre]
            if kind == 'front':
                cands.append(sqs[0])
            elif kind == 'back':
                cands.append(sqs[-1])
            elif kind == 'mid' and len(sqs) >= 3:
                cands.append(sqs[len(sqs) // 2])
            elif isinstance(kind, int) and kind <= len(sqs):
                cands.append(sqs[kind - 1])
    else:
        ptype = PIECE.get(pch)
        if not ptype or not f1:
            return None
        x = to_x(NUM[f1])
        cands = [sq for sq, p in pos.cells.items()
                 if sq[0] == x and p.upper() == ptype and (p.isupper() == (side == RED))]
    num = NUM[n]
    found = []
    for src in cands:
        d = DIRS[dch]
        if d == 0:
            dst = (to_x(num), src[1])
            if ptype in 'NAB':
                continue
        elif ptype in 'RCPK':
            dst = (src[0], src[1] + sign * d * num)
        else:
            dst = (to_x(num), None)
        for mv in legal:
            if mv[:2] != sq_name(src):
                continue
            t = parse_sq(mv[2:])
            if ptype in 'NAB' and d != 0:
                if t[0] == dst[0] and (t[1] - src[1]) * sign * d > 0:
                    found.append(mv)
            elif t == dst:
                found.append(mv)
    found = sorted(set(found))
    return found[0] if len(found) == 1 else None


TOKEN = re.compile(r'\(|\)|\d+\.|[^\s()]+')


def parse_tree(text):
    """Trả về (fen, root) với root = {'children': [...]}, mỗi nút {'m','ply','children'}.

    Lỗi (không đọc được nước) ghi trong root['errors'].
    """
    fen = re.search(r'\[FEN "([^"]*)"', text)
    fen = fen.group(1) if fen else 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR r'
    body = re.sub(r'^\[.*\]\s*$', '', text, flags=re.M)
    body = re.sub(r'\{[^}]*\}', ' ', body)
    start = Position.from_fen(fen)
    root = {'m': None, 'ply': 0, 'pos': start, 'children': [], 'errors': []}
    cur = root
    stack = []          # (nút cha của nước thay thế, nút hiện tại để khôi phục)
    dead = False        # nhánh hiện tại đã gãy -> bỏ qua đến khi gặp ")" hoặc "("
    toks = TOKEN.findall(body)
    for t in toks:
        if t == '(':
            if cur is root:
                continue
            # biến: thay nước vừa đi => quay về cha của nút cur
            parent = cur['parent']
            stack.append((cur, dead))
            cur = parent
            dead = False
        elif t == ')':
            if stack:
                cur, dead = stack.pop()
        elif re.fullmatch(r'\d+\.', t) or t in ('*', '1-0', '0-1', '1/2-1/2'):
            continue
        else:
            if dead:
                continue
            mv = resolve(cur['pos'], t)
            if not mv:
                root['errors'].append({'ply': cur['ply'] + 1, 'token': t})
                dead = True
                continue
            child = next((c for c in cur['children'] if c['m'] == mv), None)
            if child is None:
                child = {'m': mv, 'ply': cur['ply'] + 1, 'pos': cur['pos'].play(mv),
                         'children': [], 'parent': cur}
                cur['children'].append(child)
            cur = child
    return fen, root


def strip(node):
    """Bỏ trường nội bộ (pos, parent) để xuất JSON."""
    out = {'m': node['m'], 'ply': node['ply']}
    if node['children']:
        out['c'] = [strip(c) for c in node['children']]
    return out


def stats(root):
    n = lines = depth = 0
    stack = [root]
    while stack:
        x = stack.pop()
        n += 1
        depth = max(depth, x['ply'])
        if not x['children']:
            lines += 1
        stack += x['children']
    return {'nodes': n - 1, 'lines': lines, 'depth': depth, 'errors': len(root['errors'])}
