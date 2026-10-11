"""Phân tích một thế cờ tàn bằng bảng tra chessdb (không cần engine).

Đầu ra là dữ kiện thuần (không có lời bình): biến chính tối ưu, các thời điểm
then chốt (nước duy nhất, nước chờ, bị ép nước), các nước sai hấp dẫn và cách
trừng phạt, và giải phẫu thế chiếu bí cuối cùng.
"""
from __future__ import annotations

from . import cdb
from .board import RED, Position, other, parse_sq, side_of, sq_name
from .notation import short_move, vn_move

DRAW_LINE_PLIES = 16


def outcome_text(wdl, dtm):
    if wdl == 'W':
        return f'Thắng ({(dtm + 1) // 2} nước)'
    if wdl == 'L':
        return f'Thua ({dtm // 2 + 1} nước)' if dtm else 'Thua'
    return 'Hòa'


def safe_value(pos):
    """Giá trị cho bên đi; None nếu thế không hợp lệ (ví dụ bên kia đang bị chiếu)."""
    try:
        return cdb.value(Position.from_fen(pos.fen()).fen())
    except ValueError:
        return None


def describe_move(pos, move):
    src, dst = parse_sq(move[:2]), parse_sq(move[2:])
    nxt = pos.play(move)
    captured = pos.cells.get(dst)
    return {
        'move': move,
        'vn': vn_move(pos, move),
        'short': short_move(pos, move),
        'piece': pos.cells[src],
        'capture': captured,
        'check': nxt.in_check(nxt.turn),
        'mate': nxt.is_mate(),
    }


def _ranked(res):
    """Các nước kèm kết quả cho bên đi, theo thứ tự tốt → xấu."""
    def key(m):
        if m['wdl'] == 'W':
            return (0, m['dtm'])
        if m['wdl'] == 'D':
            return (1, 0)
        return (2, -m['dtm'])
    return sorted(res['moves'], key=key)


def _pick(pos, res, attacker):
    ranked = _ranked(res)
    best = ranked[0]
    if best['wdl'] == 'W':
        # Nhiều nước nhanh như nhau: ưu tiên nước có tiến triển (không phải nước Tướng/Sĩ/Tượng).
        ties = [m for m in ranked if m['wdl'] == 'W' and m['dtm'] == best['dtm']]
        active = [m for m in ties if pos.cells[parse_sq(m['move'][:2])].upper() not in 'KAB']
        return (active or ties)[0]['move']
    if best['wdl'] != 'D' or pos.turn != attacker:
        return best['move']
    # Thế hòa, bên tấn công đi: chọn nước gây khó nhất (ít nước giữ hòa nhất cho đối phương).
    best_move, best_score = best['move'], None
    for m in ranked:
        if m['wdl'] != 'D':
            break
        nxt = pos.play(m['move'])
        r = cdb.query(nxt.fen())
        if r['status'] == 'mate':
            continue
        holds = sum(x['wdl'] == 'D' for x in r['moves'])
        score = (holds, -len(r['moves']))
        if best_score is None or score < best_score:
            best_move, best_score = m['move'], score
    return best_move


def play_line(fen, attacker, max_plies=None, seen=None):
    """Biến tối ưu từ fen. Bên thắng chọn nước chiếu bí nhanh nhất, bên thua chống lâu nhất."""
    pos = Position.from_fen(fen)
    plies = []
    seen = set(seen or ())
    while True:
        res = cdb.query(pos.fen())
        if res['status'] == 'mate':
            break
        if max_plies is not None and len(plies) >= max_plies:
            break
        if pos.fen() in seen:
            break
        seen.add(pos.fen())
        move = _pick(pos, res, attacker)
        ranked = _ranked(res)
        best = ranked[0]
        chosen = next(m for m in ranked if m['move'] == move)
        good = [m for m in ranked if m['wdl'] == best['wdl']]
        if best['wdl'] == 'W':
            fastest = [m for m in good if m['dtm'] == best['dtm']]
        else:
            fastest = good
        info = describe_move(pos, move)
        info.update({
            'fen': pos.fen(),
            'side': pos.turn,
            'wdl': chosen['wdl'],
            'dtm': chosen['dtm'],
            'n_legal': len(ranked),
            'n_keep': len(good),
            'only': len(good) == 1 and len(ranked) > 1,
            'only_fastest': len(fastest) == 1 and len(good) > 1,
            'ranked': [{**m, 'vn': vn_move(pos, m['move'])} for m in ranked],
        })
        plies.append(info)
        pos = pos.play(move)
        if best['wdl'] == 'D' and max_plies is None and len(plies) >= DRAW_LINE_PLIES:
            break
    return plies, pos


TEMPT_ORDER = {'capture': 0, 'check': 1, 'advance': 2, 'same_piece': 3, 'other': 4}


def tempting(pos, ranked, chosen_move, bad):
    """Sắp các nước sai theo mức 'hấp dẫn' với người chơi: ăn quân, chiếu, cùng quân."""
    src = parse_sq(chosen_move[:2])
    out = []
    for m in bad:
        d = describe_move(pos, m['move'])
        s_, d_ = parse_sq(m['move'][:2]), parse_sq(m['move'][2:])
        fwd = (d_[1] - s_[1]) * (1 if pos.turn == RED else -1)
        kind = ('capture' if d['capture'] else 'check' if d['check'] else
                'advance' if d['piece'].upper() == 'P' and fwd > 0 else
                'same_piece' if s_ == src else 'other')
        out.append((TEMPT_ORDER[kind], d['vn'], {**m, **d, 'kind': kind}))
    return [x[2] for x in sorted(out, key=lambda t: (t[0], t[1]))]


def refutation(pos_after_mistake, attacker, plies=6):
    line, end = play_line(pos_after_mistake.fen(), attacker, max_plies=plies)
    return line, end


def zugzwang_notes(ply, attacker):
    """So sánh với trường hợp 'được bỏ lượt' bằng cách lật lượt đi rồi tra lại."""
    pos = Position.from_fen(ply['fen'])
    if pos.in_check(pos.turn):
        return None
    flipped = safe_value(pos.flip_turn())
    if flipped is None:
        return None
    me = pos.turn
    wdl_me = ply['ranked'][0]['wdl']
    flipped_for_me = {'W': 'L', 'L': 'W', 'D': 'D'}[flipped[0]]
    quiet = not ply['capture'] and not ply['check']
    if me == attacker and wdl_me == 'W' and quiet and ply['piece'].upper() in 'KAB' \
            and flipped_for_me == 'W':
        # 'key': nước chờ là cách thắng duy nhất / nhanh nhất duy nhất, không chỉ là một lựa chọn.
        return {'type': 'waiting', 'pass_dtm': flipped[1], 'key': ply['only'] or ply['only_fastest']}
    if me != attacker and wdl_me == 'L' and flipped_for_me != 'L':
        return {'type': 'zugzwang', 'pass_result': flipped_for_me}
    if me != attacker and wdl_me == 'D' and flipped_for_me == 'W':
        return {'type': 'zugzwang_draw'}
    return None


def mate_anatomy(pos):
    """Giải phẫu thế bí: bên bị bí, quân chiếu, ô thoát và quân khống chế mỗi ô."""
    loser = pos.turn
    k = pos.king_sq(loser)
    checkers = pos.checkers(loser)
    flyers = pos.kings_facing()
    squares = []
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        s = (k[0] + dx, k[1] + dy)
        if not (3 <= s[0] <= 5 and (0 <= s[1] <= 2 if loser == RED else 7 <= s[1] <= 9)):
            continue
        occ = pos.cells.get(s)
        if occ and side_of(occ) == loser:
            squares.append({'sq': sq_name(s), 'blocked_by_own': occ})
            continue
        trial = Position(pos.cells, loser)
        trial.cells[s] = trial.cells.pop(k)
        guards = [sq_name(g) + ':' + trial.cells[g] for g in trial.checkers(loser)]
        if trial.kings_facing():
            guards.append(sq_name(trial.king_sq(other(loser))) + ':' + ('K' if loser != RED else 'k')
                          + ':mặt')
        squares.append({'sq': sq_name(s), 'guards': guards})
    return {
        'loser': loser,
        'king': sq_name(k),
        'in_check': bool(checkers) or flyers,
        'checkers': [sq_name(c) + ':' + pos.cells[c] for c in checkers],
        'escapes': squares,
    }


def analyze(fen, attacker=RED, max_traps=3):
    root = Position.from_fen(fen)
    root_value = cdb.value(root.fen())
    main, end = play_line(fen, attacker)
    traps = []
    for i, ply in enumerate(main):
        z = zugzwang_notes(ply, attacker)
        if z:
            ply['zug'] = z
        pos = Position.from_fen(ply['fen'])
        best = ply['ranked'][0]['wdl']
        if best == 'W':
            bad = [m for m in ply['ranked'] if m['wdl'] != 'W']
        elif best == 'D':
            bad = [m for m in ply['ranked'] if m['wdl'] == 'L']
        else:
            bad = []
        ply['n_bad'] = len(bad)
        if not bad:
            continue
        lure = tempting(pos, ply['ranked'], ply['move'], bad)[0]
        # Chỉ trình bày khi thật sự là bẫy: ít nước giữ kết quả, hoặc nước sai rất 'hấp dẫn'.
        if ply['n_keep'] > 3 and lure['kind'] not in ('capture', 'check', 'advance'):
            continue
        after = pos.play(lure['move'])
        line, final = refutation(after, attacker, plies=6 if best == 'W' else 9)
        if best == 'W':
            # Dừng ngay khi bên phòng thủ đã có lời đáp quyết định (ăn quân / nước duy nhất).
            for j, x in enumerate(line):
                if x['side'] != ply['side'] and (x['capture'] or x['only']):
                    line = line[:j + 1]
                    break
            else:
                line = line[:2]
            final = Position.from_fen(line[-1]['fen']).play(line[-1]['move']) if line else after
        traps.append({'ply': i, 'fen': ply['fen'], 'lure': lure, 'line': line,
                      'final_fen': final.fen(), 'final_mate': final.is_mate()})
    traps.sort(key=lambda t: (main[t['ply']]['n_keep'] > 3, TEMPT_ORDER[t['lure']['kind']],
                              main[t['ply']]['n_keep'], t['ply']))
    picked, themes = [], set()
    for t in traps:
        lure = t['lure']
        theme = (lure['kind'], lure['piece'].upper(), lure['move'][3] in '09' and lure['piece'].upper() == 'P')
        if theme in themes:
            continue
        themes.add(theme)
        picked.append(t)
    traps = sorted(picked[:max_traps], key=lambda t: t['ply'])
    return {
        'fen': root.fen(),
        'attacker': attacker,
        'value': {'wdl': root_value[0], 'dtm': root_value[1]},
        'main': main,
        'end_fen': end.fen(),
        'mate': mate_anatomy(end) if end.is_mate() else None,
        'traps': traps,
    }
