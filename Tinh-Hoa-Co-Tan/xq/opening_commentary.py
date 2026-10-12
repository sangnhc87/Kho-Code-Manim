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
            if q != sq and side_of(p) == me and p.upper() != 'K' and pos.attacks(sq, q)]


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
    """Các mệnh đề mục đích, theo thứ tự ưu tiên."""
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
        if recapture and VALUE[victim.upper()] <= VALUE[u]:
            out.append(f'{name(piece)} ăn {name(victim)}, hai bên sẽ đổi quân' if VALUE[victim.upper()] >= VALUE[u]
                       else f'{name(piece)} ăn {name(victim)} nhưng bị ăn lại')
        else:
            out.append(f'{name(piece)} ăn {name(victim)} của {foe}')
    if new.in_check(new.turn):
        out.append(f'chiếu Tướng {foe}')
    threats = [(q, p, d) for q, p, d in attacked_enemy(new, dst) if VALUE[p.upper()] >= 4 and (q != dst)]
    loose = [name(p) for q, p, d in threats if not d]
    if loose and not victim:
        out.append(f'đe dọa ăn {loose[0]} chưa được bảo vệ')
    elif threats and not victim and not loose:
        out.append(f'gây sức ép lên {name(threats[0][1])} của {foe}')
    if u == 'C' and dst[0] == 4 and src[0] != 4:
        out.append('đưa Pháo vào lộ giữa, nhắm vào Tốt đầu và cung đối phương')
    elif u == 'N' and src in HOME['N']:
        guards = [name(p) for q, p in defended_friends(new, dst)][:2]
        out.append('nhảy Mã ra quân' + (f', bảo vệ {" và ".join(guards)}' if guards else ''))
    elif u == 'R' and src in HOME['R']:
        n = file_no(dst[0], side)
        block = file_open_ahead(new, dst, side)
        out.append(f'xuất Xe, chiếm lộ {n}' + (', lộ này thông tới tận đáy đối phương' if block is None else ''))
    elif u == 'R' and ((dst[1] > 4) if side == RED else (dst[1] < 5)) and ((src[1] <= 4) if side == RED else (src[1] >= 5)):
        out.append('Xe vượt sông, ép vào thế trận đối phương')
    elif u == 'R' and src[0] != dst[0]:
        out.append(f'Xe chuyển sang lộ {file_no(dst[0], side)}')
    elif u == 'P':
        crossing = (dst[1] > 4 and src[1] <= 4) if side == RED else (dst[1] < 5 and src[1] >= 5)
        out.append('Tốt qua sông, tăng sức công kích' if crossing else 'tiến Tốt mở đường cho Mã và Xe')
    elif u in 'AB':
        out.append('củng cố phòng ngự quanh Tướng')
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
            if best == move:
                notes.append('Đây cũng là nước máy chọn đầu tiên')
            elif best and loss >= 60:
                notes.append(f'Máy đánh giá {vn_move(pos, best)} tốt hơn khoảng {int(loss)} điểm, '
                             f'nhưng biến này vẫn thuộc lý thuyết khai cục')
            elif best and loss < 25:
                notes.append(f'Máy cho điểm gần ngang nước mạnh nhất {vn_move(pos, best)}')
    return parts, notes


def sentence(parts):
    if not parts:
        return ''
    s = parts[0][0].upper() + parts[0][1:]
    if len(parts) > 1:
        s += ', ' + ', '.join(parts[1:3])
    return s + '.'
