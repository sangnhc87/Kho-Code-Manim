"""Biến dữ kiện phân tích (xq.analyze) thành kịch bản video có lời bình tiếng Việt.

Mọi nhận định trong lời bình đều suy ra từ bảng tra: thắng/hòa, số nước đến bí,
nước duy nhất, nước chờ, bị ép nước, nước sai và cách trừng phạt. Không có câu
nào khẳng định điều bảng tra không xác nhận.
"""
from __future__ import annotations

import hashlib
import random

from .board import RED, Position, parse_sq, side_of
from .notation import piece_name

SIDE = {'w': 'Đỏ', 'b': 'Đen'}
PIECE_WORD = {'K': 'Tướng', 'A': 'Sĩ', 'B': 'Tượng', 'N': 'Mã', 'R': 'Xe', 'C': 'Pháo', 'P': 'Tốt'}


def word(piece):
    """Tên quân theo đúng bên: Binh cho Đỏ, Tốt cho Đen."""
    return piece_name(piece)


def file_word(x, side=RED):
    return 9 - x if side == RED else x + 1


def facing_files(pos):
    """Ô trong cung Đen mà Tướng Đen không được bước vào vì lộ mặt Tướng Đỏ."""
    k = pos.king_sq(RED)
    out = []
    for y in range(7, 10):
        sq = (k[0], y)
        if not 3 <= k[0] <= 5:
            continue
        between = [(k[0], j) for j in range(k[1] + 1, y)]
        if not any(b in pos.cells for b in between) and pos.cells.get(sq) in (None, 'k'):
            out.append(sq)
    return out


def moves_count(dtm):
    """Số nước của bên thắng tương ứng DTM tính theo nước nửa."""
    return (dtm + 1) // 2


def material_words(pos, side):
    order = 'KRCNABP'
    counts = {}
    for p in pos.cells.values():
        if side_of(p) == side:
            counts[p.upper()] = counts.get(p.upper(), 0) + 1
    words = []
    for u in sorted(counts, key=order.index):
        name = piece_name(u if side == RED else u.lower())
        n = counts[u]
        words.append(name if n == 1 else f'{("hai", "ba", "bốn", "năm")[n - 2]} {name}')
    return ', '.join(words)


def king_room(pos, side):
    """Số ô Tướng của side có thể đi (đếm trong thế side được đi)."""
    trial = Position(pos.cells, side)
    k = trial.king_sq(side)
    return sum(1 for m in trial.legal_moves() if parse_sq(m[:2]) == k)


class Writer:
    def __init__(self, seed):
        self.rng = random.Random(int(hashlib.sha1(seed.encode()).hexdigest()[:8], 16))

    def pick(self, *options):
        return self.rng.choice(options)


def outcome_phrase(wdl, dtm, side_word='Đỏ'):
    if wdl == 'W':
        return f'{side_word} thắng, chiếu bí sau {moves_count(dtm)} nước'
    if wdl == 'D':
        return 'kết quả chỉ là hòa'
    return f'{side_word} thua'


def candidate_rows(ply, limit=6):
    ranked = ply['ranked']
    rows, seen = [], set()
    wins = [m for m in ranked if m['wdl'] == 'W']
    others = [m for m in ranked if m['wdl'] != 'W']
    for m in wins[:limit - min(2, len(others))] + others[:2]:
        if m['move'] in seen:
            continue
        seen.add(m['move'])
        if m['wdl'] == 'W':
            res = f'Thắng – bí sau {moves_count(m["dtm"])} nước'
        elif m['wdl'] == 'D':
            res = 'Hòa'
        else:
            res = 'Thua'
        rows.append({'move': m['move'], 'vn': m['vn'], 'wdl': m['wdl'], 'result': res,
                     'best': m['move'] == ply['move']})
    return rows


def _attacker_say(w, ply, nxt_ply, pos_after, trap_here):
    vn = ply['vn']
    bits = []
    if ply['mate']:
        if pos_after.in_check(pos_after.turn):
            return f'{vn}. Chiếu bí! Đen hết đường chạy, Đỏ giành chiến thắng.'
        return f'{vn}. Đen tuy không bị chiếu nhưng đã hết nước đi hợp lệ, theo luật cờ tướng là thua cờ.'
    if ply['capture']:
        bits.append(f'ăn {word(ply["capture"])}')
    if ply['check']:
        bits.append('chiếu Tướng')
    head = f'{vn}' + (f', {" và ".join(bits)}.' if bits else '.')
    reason = []
    zug = ply.get('zug')
    before = Position.from_fen(ply['fen'])
    if zug and zug['type'] == 'waiting' and zug.get('key'):
        reason.append(w.pick(
            'Đây là nước chờ: Đỏ không tấn công gì thêm, chỉ trao lượt cho Đen. Bảng tra cho biết nếu Đen phải đi ở thế này thì Đen thua.',
            'Một nước chờ rất tinh tế. Đỏ cố ý nhường lượt, vì ở thế này bên phải đi chính là Đen, và Đen không giữ nổi thế thủ.'))
    elif zug and zug['type'] == 'waiting' and w.rng.random() < .5:
        reason.append('Đỏ có thể nhường lượt ở đây, vì Đen phải đi thì thế thủ càng xấu.')
    if ply['piece'] == 'K' and not ply['check']:
        new_face = set(facing_files(pos_after)) - set(facing_files(before))
        bk = pos_after.king_sq('b')
        if new_face and bk[0] != parse_sq(ply['move'][2:])[0]:
            reason.append(f'Tướng Đỏ chiếm lộ {file_word(parse_sq(ply["move"][2:])[0])}, '
                          'nhờ luật lộ mặt tướng mà Tướng Đen không thể bước sang lộ này.')
    if ply['piece'] == 'P' and not ply['check'] and not ply['capture']:
        d = parse_sq(ply['move'][2:])
        if 3 <= d[0] <= 5 and d[1] >= 7 and not any(3 <= sq[0] <= 5 and sq[1] >= 7 and p == 'P'
                                                    for sq, p in before.cells.items()):
            reason.append('Binh đã áp sát cung Đen.')
    if ply['only']:
        if trap_here:
            reason.append(f'Đây là nước duy nhất giữ được thắng lợi; ví dụ nếu đi {trap_here["lure"]["vn"]} thì {outcome_phrase(trap_here["lure"]["wdl"], trap_here["lure"]["dtm"])}.')
        else:
            reason.append('Đây là nước duy nhất giữ được thắng lợi, mọi nước khác đều để Đen thoát hòa.')
    elif ply['n_keep'] <= 3 and ply['n_keep'] < ply['n_legal']:
        reason.append(w.pick(f'Chỉ có {ply["n_keep"]} nước giữ được thắng ở thời điểm này.',
                             f'Cần chính xác: chỉ {ply["n_keep"]} trong {ply["n_legal"]} nước còn thắng.'))
    elif ply['only_fastest'] and not reason and w.rng.random() < .35:
        reason.append('Đây là con đường ngắn nhất đến chiếu bí.')
    room = king_room(pos_after, 'b') if not ply['mate'] else 0
    if not reason and room <= 1 and nxt_ply is not None and w.rng.random() < .6:
        reason.append('Tướng Đen chỉ còn ' + ('đúng một ô để di chuyển.' if room == 1 else 'không còn ô nào để đi, chỉ có thể đi quân khác.'))
    return ' '.join([head] + reason)


def _defender_say(w, ply):
    vn = ply['vn']
    plain = w.pick(f'Đen đi {vn}.', f'Đen đáp {vn}.', f'{vn}.')
    zug = ply.get('zug')
    if ply['n_legal'] == 1:
        return w.pick(f'Đen chỉ có một nước hợp lệ: {vn}.', f'Bắt buộc: {vn}.')
    if zug and zug['type'] == 'zugzwang':
        return (f'Đen bị ép nước. Nếu được bỏ lượt thì Đen {"hòa" if zug["pass_result"] == "D" else "thoát nguy"}, '
                f'nhưng luật bắt buộc phải đi, nên đành {vn}.')
    if ply['wdl'] == 'D':
        if ply['only']:
            return f'{vn}. Nước duy nhất giữ hòa của Đen.'
        return f'{vn}, Đen giữ thế hòa.'
    if ply['capture']:
        return f'{vn}, Đen ăn {word(ply["capture"])}.'
    longest = [m for m in ply['ranked'] if m['wdl'] == 'L' and m['dtm'] == ply['dtm']]
    if ply['n_legal'] > 1 and len(longest) == 1 and ply['ranked'][-1]['dtm'] < ply['dtm'] and w.rng.random() < .5:
        return f'{vn}. Đây là cách chống đỡ dai nhất, các nước khác thua nhanh hơn.'
    return plain


def build_episode(analysis, topic, ep, writer_seed=None):
    """analysis: kết quả xq.analyze.analyze; topic: mục trong curriculum; ep: số tập."""
    w = Writer(writer_seed or f'{topic["id"]}-{ep}')
    main = analysis['main']
    root = Position.from_fen(analysis['fen'])
    val = analysis['value']
    traps_by_ply = {t['ply']: t for t in analysis['traps']}
    first = main[0]
    n_moves = moves_count(val['dtm']) if val['wdl'] == 'W' else None
    waits = [p for p in main if p.get('zug', {}).get('type') == 'waiting' and p['zug'].get('key')]
    zugs = [p for p in main if p.get('zug', {}).get('type') == 'zugzwang']
    onlys = [p for p in main if p['side'] == analysis['attacker'] and p['only']]

    beats = []
    red_mat, black_mat = material_words(root, 'w'), material_words(root, 'b')
    beats.append({
        'kind': 'intro', 'label': 'THẾ CỜ', 'headline': topic['title'],
        'panel': {'bullets': [f'Đỏ: {red_mat}', f'Đen: {black_mat}',
                              f'{SIDE[root.turn]} đi trước']},
        'fen': analysis['fen'],
        'steps': [{'say': f'Chào mừng các bạn đến với Tinh Hoa Cờ Tàn, tập {ep}. '
                          f'Chủ đề hôm nay: {topic["title"]}. '
                          f'Bên Đỏ còn {red_mat}; bên Đen còn {black_mat}. {SIDE[root.turn]} đi trước.'}],
    })
    beats.append({
        'kind': 'theory', 'label': 'KIẾN THỨC NỀN', 'headline': topic['short'],
        'panel': {'bullets': topic['bullets']},
        'steps': [{'say': s} for s in topic['theory']],
    })
    q = ('Đỏ đi trước có thắng được không, và nước đầu tiên là gì?' if val['wdl'] == 'W'
         else 'Đỏ có thắng được không? Đen phải phòng thủ thế nào?')
    beats.append({
        'kind': 'puzzle', 'label': 'THỬ THÁCH', 'headline': 'Bạn sẽ đi thế nào?',
        'panel': {'countdown': 5},
        'steps': [{'say': f'Trước khi xem lời giải, bạn hãy tạm dừng video và tự suy nghĩ. {q}'}],
    })
    rows = candidate_rows(first)
    wins = sum(1 for m in first['ranked'] if m['wdl'] == 'W')
    say = [f'Theo bảng tra cờ tàn của chessdb, thế cờ này {outcome_phrase(val["wdl"], val["dtm"])} nếu hai bên cùng chơi chính xác.']
    if val['wdl'] == 'W':
        speeds = {m['dtm'] for m in first['ranked'] if m['wdl'] == 'W'}
        if wins == first['n_legal']:
            say.append(f'Đỏ có {first["n_legal"]} nước hợp lệ và nước nào cũng còn thắng' +
                       (', nhưng tốc độ khác nhau.' if len(speeds) > 1 else '.'))
        elif wins == 1:
            say.append(f'Trong {first["n_legal"]} nước hợp lệ, chỉ có đúng một nước thắng: {first["vn"]}.')
        else:
            say.append(f'Trong {first["n_legal"]} nước hợp lệ, chỉ {wins} nước còn thắng.')
        fastest = [m for m in first['ranked'] if m['wdl'] == 'W' and m['dtm'] == val['dtm']]
        if wins > 1:
            say.append(f'Nhanh nhất là {first["vn"]}.' if len(fastest) == 1 else
                       f'Có {len(fastest)} nước thắng nhanh như nhau; ta chọn {first["vn"]}.')
        draws = [r['vn'] for r in rows if r['wdl'] == 'D']
        losses = [r['vn'] for r in rows if r['wdl'] == 'L']
        if draws:
            say.append(f'Còn nếu đi {" hay ".join(draws[:2])} thì {"đều " if len(draws) > 1 else ""}chỉ hòa.')
        if losses:
            say.append(f'Đi {losses[0]} thì Đỏ còn thua.')
    beats.append({'kind': 'candidates', 'label': 'BẢNG TRA', 'headline': 'So sánh các nước đầu',
                  'panel': {'rows': rows}, 'steps': [{'say': ' '.join(say)}]})

    if 0 in traps_by_ply:
        beats.append(_trap_beat(w, traps_by_ply[0], main))

    # ---- biến chính, chia thành từng chặng ----
    chunk, chunks = [], []
    for i, ply in enumerate(main):
        chunk.append(i)
        key = ply['only'] or ply.get('zug') or ply['capture']
        if ((i + 1) in traps_by_ply or i == len(main) - 1
                or (ply['side'] != analysis['attacker'] and (len(chunk) >= 6 or key))):
            chunks.append(chunk)
            chunk = []
    if chunk:
        chunks.append(chunk)
    for c_idx, idxs in enumerate(chunks):
        steps = []
        for i in idxs:
            ply = main[i]
            pos_after = Position.from_fen(ply['fen']).play(ply['move'])
            nxt = main[i + 1] if i + 1 < len(main) else None
            if ply['side'] == analysis['attacker']:
                say = _attacker_say(w, ply, nxt, pos_after, traps_by_ply.get(i))
            else:
                say = _defender_say(w, ply)
            mark = 'only' if ply['only'] and ply['side'] == analysis['attacker'] else \
                   ('wait' if ply.get('zug', {}).get('type') == 'waiting' and ply['zug'].get('key') else
                    'zug' if ply.get('zug', {}).get('type') == 'zugzwang' else None)
            steps.append({'say': say, 'move': ply['move'], 'ply': i, 'mark': mark,
                          'remain': ply['dtm'] if ply['wdl'] != 'D' else None})
        head_ply = next((main[i] for i in idxs if main[i]['only'] and main[i]['side'] == analysis['attacker']), None)
        if c_idx == 0:
            headline = 'Nước mở đầu then chốt' if first['only'] else 'Bắt đầu ép cung'
        elif any(main[i]['mate'] for i in idxs):
            headline = 'Đòn kết thúc'
        elif head_ply:
            headline = 'Nước duy nhất!'
        elif any(main[i].get('zug', {}).get('type') == 'waiting' and main[i]['zug'].get('key') for i in idxs):
            headline = 'Nước chờ tinh tế'
        elif any(main[i].get('zug', {}).get('type') == 'zugzwang' for i in idxs):
            headline = 'Đen bị ép nước'
        elif any(main[i]['capture'] for i in idxs):
            headline = 'Thu hoạch vật chất'
        else:
            headline = w.pick('Siết chặt vòng vây', 'Từng bước thu hẹp', 'Tiếp tục ép cung')
        beats.append({'kind': 'line', 'label': f'BIẾN CHÍNH • CHẶNG {c_idx + 1}', 'headline': headline,
                      'fen': main[idxs[0]]['fen'] if c_idx == 0 else None, 'steps': steps})
        # Bẫy gắn với nước đầu của chặng kế tiếp được trình bày ngay sau chặng này.
        nxt_first = idxs[-1] + 1
        if nxt_first in traps_by_ply:
            beats.append(_trap_beat(w, traps_by_ply[nxt_first], main))

    if analysis.get('mate'):
        beats.append(_mate_beat(analysis))
    beats.append(_summary_beat(topic, analysis, first, waits, zugs, onlys, n_moves))
    return beats


def _trap_beat(w, trap, main):
    lure = trap['lure']
    ply = main[trap['ply']]
    side = SIDE[ply['side']]
    kind = {'capture': 'ăn quân ngay, trông rất hấp dẫn', 'check': 'một nước chiếu trông rất mạnh',
            'advance': 'đẩy Binh tiến lên, trông rất tự nhiên',
            'same_piece': 'một nước tự nhiên', 'other': 'một nước tưởng chừng vô hại'}[lure['kind']]
    if lure['piece'] == 'P' and lure['move'][3] == '9':
        kind = 'đẩy Binh xuống tận đáy'
    if lure['wdl'] == 'D':
        verdict = f'{side} mất thắng, ván cờ trở thành hòa'
    elif lure['wdl'] == 'L':
        verdict = f'{side} bị chiếu bí sau {lure["dtm"] // 2 + 1} nước'
    else:
        verdict = f'{side} vẫn thắng nhưng chậm hơn hẳn'
    steps = [{'say': f'Dừng lại một chút. Ở thế này nếu {side} đi {lure["vn"]}, {kind}, thì sao? '
                     f'Bảng tra trả lời: {verdict}.'}]
    steps.append({'say': f'{lure["vn"]}.', 'move': lure['move'], 'mark': 'bad'})
    for x in trap['line']:
        cap = f', ăn {word(x["capture"])}' if x['capture'] else ''
        if x['side'] != ply['side'] and x['only']:
            say = f'{x["vn"]}{cap}! Nước duy nhất, và chính là lời đáp chính xác.'
        elif x['side'] != ply['side'] and x['capture']:
            say = f'{x["vn"]}{cap}!'
        else:
            say = f'{x["vn"]}{cap}.'
        if x['mate']:
            say = f'{x["vn"]}. Hết cờ.'
        steps.append({'say': say, 'move': x['move']})
    if lure['wdl'] == 'D' and lure['piece'] == 'P' and lure['move'][3] == '9':
        tail = ('Binh đã xuống đáy thành Binh già, không bao giờ lùi lại được, và chiến thắng tan biến. '
                'Quay lại biến chính.')
    elif lure['wdl'] == 'D':
        tail = 'Chỉ một nước thiếu chính xác là công sức cả ván đổ sông đổ biển. Quay lại biến chính.'
    else:
        tail = 'Quay lại biến chính.'
    steps.append({'say': tail})
    return {'kind': 'trap', 'label': 'BẪY CẦN TRÁNH', 'headline': f'Nếu {lure["vn"]}?',
            'fen': trap['fen'], 'return_fen': trap['fen'], 'steps': steps,
            'panel': {'verdict': verdict}}


def _mate_beat(analysis):
    mate = analysis['mate']
    pieces = {'N': 0, 'R': 0, 'C': 0, 'P': 0, 'K': 0, 'face': 0, 'own': 0}
    for e in mate['escapes']:
        if 'blocked_by_own' in e:
            pieces['own'] += 1
            continue
        for g in e['guards']:
            if g.endswith(':mặt'):
                pieces['face'] += 1
            else:
                pieces[g.split(':')[1].upper()] += 1
    parts = []
    if mate['in_check']:
        who = ', '.join(word(c.split(':')[1]) for c in mate['checkers']) or 'mặt Tướng'
        parts.append(f'Tướng Đen đang bị {who} chiếu.')
    else:
        parts.append('Tướng Đen không bị chiếu, nhưng bên Đen không còn nước đi hợp lệ nào.')
    guard_words = []
    for u in ('R', 'N', 'C', 'P'):
        if pieces[u]:
            guard_words.append(f'{pieces[u]} ô bị {word(u)} Đỏ khống chế')
    if pieces['face']:
        guard_words.append(f'{pieces["face"]} ô bị Tướng Đỏ khống chế theo luật lộ mặt tướng')
    if pieces['own']:
        guard_words.append(f'{pieces["own"]} ô bị chính quân Đen chặn')
    if guard_words:
        parts.append('Các ô thoát quanh Tướng Đen: ' + '; '.join(guard_words) + '.')
    if pieces['face']:
        parts.append('Hãy nhớ: trong cờ tàn, Tướng không chỉ để phòng thủ. Chiếm đúng lộ, Tướng trở thành một quân tấn công thực thụ.')
    return {'kind': 'mate', 'label': 'GIẢI PHẪU THẾ BÍ', 'headline': 'Vì sao Đen hết đường?',
            'steps': [{'say': ' '.join(parts)}], 'panel': {'mate': mate}}


def _summary_beat(topic, analysis, first, waits, zugs, onlys, n_moves):
    bullets, say = [], []
    if n_moves:
        bullets.append(f'Kết quả: Đỏ thắng, bí sau {n_moves} nước')
        say.append(f'Tóm tắt bài học. Thế cờ này Đỏ thắng, chiếu bí sau {n_moves} nước khi hai bên chơi tối ưu.')
    else:
        bullets.append('Kết quả: Hòa nếu Đen phòng thủ chính xác')
        say.append('Tóm tắt bài học. Với phòng thủ chính xác, Đen giữ được hòa.')
    bullets.append(f'Nước đầu: {first["vn"]}')
    if onlys:
        bullets.append(f'{len(onlys)} thời điểm Đỏ chỉ có một nước thắng')
        say.append(f'Trên đường thắng có {len(onlys)} thời điểm Đỏ chỉ có đúng một nước giữ được thắng lợi, đó là những chỗ cần ghi nhớ.')
    if waits:
        bullets.append('Biết dùng nước chờ để trao lượt')
        say.append('Kỹ thuật nước chờ, tức là trao lượt cho đối phương khi họ đang ở thế bất lợi, xuất hiện ' +
                   ('một lần.' if len(waits) == 1 else f'{len(waits)} lần.'))
    if zugs:
        bullets.append('Đen thua vì bị ép nước')
    bullets.append(topic['takeaway_short'])
    say.append(topic['takeaway'])
    say.append('Nếu thấy bài học hữu ích, hãy bấm thích, đăng ký kênh và chia sẻ cho bạn cờ. Hẹn gặp lại ở tập sau.')
    return {'kind': 'summary', 'label': 'TỔNG KẾT', 'headline': 'Ghi nhớ', 'panel': {'bullets': bullets},
            'steps': [{'say': s} for s in say]}
