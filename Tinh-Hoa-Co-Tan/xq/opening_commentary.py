"""Lời bình khai cục: mỗi nhận định đều suy ra từ thế cờ (hình học) hoặc từ điểm Pikafish.

explain(pos, move, ev) trả về các mệnh đề tiếng Việt về mục đích nước đi (nhảy Mã bảo vệ quân nào,
Xe chiếm lộ nào, đe dọa ăn quân nào chưa được bảo vệ, đổi quân...) và, nếu có điểm máy,
độ lệch so với nước máy chọn. Không có mệnh đề nào khẳng định điều dữ liệu không chứng minh.
"""
from __future__ import annotations

import hashlib
import random

from .board import RED, Position, parse_sq, side_of
from .notation import piece_name, vn_move

SIDE = {'w': 'Đỏ', 'b': 'Đen'}
HOME = {'R': {(0, 0), (8, 0), (0, 9), (8, 9)}, 'N': {(1, 0), (7, 0), (1, 9), (7, 9)},
        'C': {(1, 2), (7, 2), (1, 7), (7, 7)}}
VALUE = {'R': 9, 'C': 4.5, 'N': 4, 'B': 2, 'A': 2, 'P': 1, 'K': 100}


def name(piece):
    return piece_name(piece)


def file_no(x, side):
    return 9 - x if side == RED else x + 1


def red_cp(entry):
    """Điểm góc nhìn Đỏ của dòng tốt nhất (mate quy về ±10000 - n), hoặc None."""
    if not entry or not entry.get('lines'):
        return None
    ln = entry['lines'][0]
    if 'mate' in ln:
        n = ln['mate']
        return (10000 - abs(n)) * (1 if n > 0 else -1)
    return ln['cp']


def grade(cp):
    """Mô tả thế trận theo điểm góc nhìn Đỏ."""
    if cp is None:
        return None
    a = abs(cp)
    side = 'Đỏ' if cp > 0 else 'Đen'
    if a >= 9000:
        return f'{side} có đường chiếu bí'
    if a < 25:
        return 'thế cờ cân bằng'
    if a < 70:
        return f'{side} nhỉnh hơn một chút'
    if a < 150:
        return f'{side} hơn nhẹ'
    if a < 300:
        return f'{side} chiếm ưu thế rõ'
    return f'{side} chiếm ưu thế lớn'


def attacked_enemy(pos, sq):
    """Quân đối phương mà quân ở sq đang khống chế: [(sq, piece, defended)]."""
    me = side_of(pos.cells[sq])
    out = []
    for q, p in pos.cells.items():
        if side_of(p) == me or p.upper() == 'K':
            continue
        if pos.attacks(sq, q):
            defended = any(r != q and side_of(pp) != me and pos.attacks(r, q) for r, pp in pos.cells.items())
            out.append((q, p, defended))
    return out


def defended_friends(pos, sq):
    me = side_of(pos.cells[sq])
    return [(q, p) for q, p in pos.cells.items()
            if q != sq and side_of(p) == me and p.upper() in 'RCNP' and pos.attacks(sq, q)]


def desc(piece, sq):
    """'Binh lộ 5' – gọi quân theo lộ để người nghe định vị được."""
    side = side_of(piece)
    who = '' if piece.upper() == 'P' else f' {SIDE[side]}'
    return f'{name(piece)}{who} lộ {file_no(sq[0], side)}'


def file_open_ahead(pos, sq, side):
    """Có quân nào chắn trên đường thẳng của Xe tới đáy đối phương?"""
    step = 1 if side == RED else -1
    y = sq[1] + step
    while 0 <= y <= 9:
        if (sq[0], y) in pos.cells:
            return pos.cells[(sq[0], y)]
        y += step
    return None


def clauses(pos, move):
    """Các mệnh đề mục đích, theo thứ tự ưu tiên (tối đa 3 được đọc)."""
    src, dst = parse_sq(move[:2]), parse_sq(move[2:])
    piece = pos.cells[src]
    side = side_of(piece)
    u = piece.upper()
    foe = SIDE['b' if side == RED else 'w']
    victim = pos.cells.get(dst)
    new = pos.play(move)
    out = []
    if victim:
        recapture = any(side_of(p) != side and new.attacks(q, dst) for q, p in new.cells.items())
        if recapture and VALUE[victim.upper()] >= VALUE[u]:
            out.append(f'{name(piece)} ăn {desc(victim, dst)}, bên kia sẽ ăn lại nên đây là nước đổi quân')
        elif recapture:
            out.append(f'{name(piece)} ăn {desc(victim, dst)} nhưng có thể bị ăn lại, nên phải tính kỹ')
        else:
            out.append(f'{name(piece)} ăn {desc(victim, dst)} mà không bị ăn lại')
    if new.in_check(new.turn):
        out.append(f'chiếu Tướng {foe}')
    threats = [(q, p, d) for q, p, d in attacked_enemy(new, dst) if q != dst]
    big = [(q, p, d) for q, p, d in threats if VALUE[p.upper()] >= 4]
    loose = [desc(p, q) for q, p, d in big if not d]
    if loose and not victim:
        out.append(f'đe dọa ăn {loose[0]}')
    elif big and not victim:
        out.append(f'gây sức ép lên {desc(big[0][1], big[0][0])}')
    if u == 'C' and dst[0] == 4 and src[0] != 4:
        rival = any(p == ('c' if side == RED else 'C') and q[0] == 4 for q, p in pos.cells.items())
        out.append('Pháo đối Pháo: hai Pháo nhìn thẳng nhau trên lộ giữa' if rival else
                   'đưa Pháo vào lộ giữa, nhắm vào Tốt đầu của đối phương')
    elif u == 'N' and src in HOME['N']:
        guards = []
        for q, p in defended_friends(new, dst):
            d = desc(p, q)
            if d not in guards:
                guards.append(d)
        out.append('nhảy Mã ra quân' + (f', bảo vệ {" và ".join(guards[:2])}' if guards else ''))
    elif u == 'R' and src in HOME['R']:
        n = file_no(dst[0], side)
        block = file_open_ahead(new, dst, side)
        out.append(f'xuất Xe, chiếm lộ {n}' + (', lộ này thông thẳng tới đáy đối phương' if block is None else
                                                f', phía trước còn {desc(block, (dst[0], 0))}' if False else ''))
    elif u == 'R' and ((dst[1] > 4) if side == RED else (dst[1] < 5)) and ((src[1] <= 4) if side == RED else (src[1] >= 5)):
        out.append('Xe qua hà, đặt áp lực thẳng vào thế trận đối phương')
    elif u == 'R' and dst[1] == (4 if side == RED else 5) and src[1] != dst[1]:
        out.append('Xe tuần hà, canh giữ bờ sông và sẵn sàng sang cánh')
    elif u == 'P' and ((dst[1] > 4 and src[1] <= 4) if side == RED else (dst[1] < 5 and src[1] >= 5)):
        out.append(f'{name(piece)} qua sông, mở thêm hướng tấn công')
    return out


def explain(pos, move, ev=None, rng=None):
    """Danh sách câu bình cho nước move trong thế pos. ev = bảng điểm {fen: entry} (có thể None)."""
    parts = clauses(pos, move)
    notes = []
    if ev:
        before = ev.get(pos.fen())
        after = ev.get(pos.play(move).fen())
        b, a = red_cp(before), red_cp(after)
        if b is not None and a is not None and before['lines']:
            sign = 1 if pos.turn == RED else -1
            loss = (b - a) * sign
            best = before['lines'][0]['pv'][0] if before['lines'][0].get('pv') else None
            if best and best != move and loss >= 150:
                gap = str(round(loss / 100, 1)).replace('.', ',')
                notes.append(f'Lưu ý, máy cho rằng {vn_move(pos, best)} mạnh hơn khoảng {gap} điểm, '
                             f'nên biến này còn chỗ để cải tiến')
    return parts, notes


def sentence(parts):
    if not parts:
        return ''
    s = parts[0][0].upper() + parts[0][1:]
    if len(parts) > 1:
        s += ', ' + ', '.join(parts[1:3])
    return s + '.'


def rank_choices(pos, moves, ev):
    """Xếp các nước moves của bên đang đi theo điểm máy: [(vn, cp_đỏ)] từ tốt nhất; None nếu thiếu dữ liệu."""
    if not ev:
        return None
    rows = []
    for m in moves:
        cp = red_cp(ev.get(pos.play(m).fen()))
        if cp is None:
            return None
        rows.append((vn_move(pos, m), cp))
    rows.sort(key=lambda r: -r[1] if pos.turn == RED else r[1])
    return rows


def fmt(cp):
    return f'{cp / 100:+.2f}'.replace('.', ',')


def exchange_words(pos, moves):
    """Các lần ăn quân trong chuỗi nước: ['Xe Đỏ ăn Pháo Đen', ...] (chỉ hình học, không đoán)."""
    out = []
    for m in moves:
        victim = pos.cells.get(parse_sq(m[2:]))
        if victim:
            p = pos.cells[parse_sq(m[:2])]
            out.append(f'{name(p)} {SIDE[side_of(p)]} ăn {name(victim)} {SIDE[side_of(victim)]}')
        pos = pos.play(m)
    return out


def spoken_cp(cp):
    """Đọc điểm máy thành lời: 'Đỏ hơn 0,44' / 'Đen hơn 0,12' / 'cân bằng'."""
    if abs(cp) < 5:
        return 'cân bằng'
    return f'{"Đỏ" if cp > 0 else "Đen"} hơn {abs(cp) / 100:.2f}'.replace('.', ',')
