#!/usr/bin/env python3
"""Dựng kịch bản tập khai cục (video dài) từ cây biến + điểm Pikafish + lý thuyết viết tay.

python scripts/build_khaicuc_episode.py --opening thuanphao --part 1 [--budget 300] [--number 1]
-> khaicuc/episodes/kc-<number>.json  (chia chương ~6-8 phút để render song song trên Actions)
Cây biến duyệt theo chiều sâu: biến chính trước, rồi các biến phụ từ nút sâu nhất ngược lên.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from xq.board import Position  # noqa: E402
from xq.notation import vn_move  # noqa: E402
from xq.opening_commentary import (SIDE, exchange_words, explain, fmt, grade, rank_choices, red_cp,  # noqa: E402
                                   sentence, spoken_cp)

WPS = 3.9            # từ/giây của giọng đọc (Thiện Minh ~4,2)
STEP_PAD = 1.5       # giây hoạt ảnh mỗi nước
GAP_MOVE, GAP_TALK = 1.6, 2.0   # nhịp nghỉ sau mỗi câu (cảnh Manim cộng thêm đúng số này)
CHAPTER_SECONDS = 420
SWING = 90           # điểm lệch (centipawn) coi là bước ngoặt


def segments(tree, start):
    """Danh sách đoạn biến: mỗi đoạn là một chuỗi nút đi theo con đầu tiên đến lá."""
    out = []

    def chain(node, pos, prefix, branch_from):
        nodes, cur, p = [], node, pos
        alts = []
        while cur.get('c'):
            kids = cur['c']
            for alt in kids[1:]:
                alts.append((len(nodes), alt, p, kids[0]))
            c = kids[0]
            nodes.append({'m': c['m'], 'ply': c['ply'], 'pos': p, 'kids': [k['m'] for k in kids]})
            p = p.play(c['m'])
            cur = c
        out.append({'prefix': list(prefix), 'branch': branch_from, 'start': pos, 'nodes': nodes})
        # biến phụ: từ nút sâu nhất ngược lên
        for idx, alt, bpos, main_kid in reversed(alts):
            pref = prefix + [(n['ply'], n['pos'], n['m']) for n in nodes[:idx]]
            # alt là nút con thay thế: đoạn mới bắt đầu bằng chính nó
            wrapper = {'c': [alt]}
            chain(wrapper, bpos, pref, {'main': main_kid['m'], 'pos': bpos, 'kids': nodes[idx]['kids']})

    chain(tree, start, [], None)
    return out


def words(text):
    return len(re.findall(r'\w+', text))


def est(step):
    return (words(step['say']) / WPS + (STEP_PAD + GAP_MOVE if step.get('move') else 0.4 + GAP_TALK)
            + step.get('countdown', 0))


def hist(prefix):
    """'5. Xe 1 bình 2' của nước cuối trước điểm rẽ."""
    if not prefix:
        return None
    ply, pos, m = prefix[-1]
    return f'nước {(ply + 1) // 2}, {SIDE[pos.turn]} đi {vn_move(pos, m)}'


def ranking_rows(pos, kids, ev):
    rows = rank_choices(pos, kids, ev)
    if not rows:
        return None, None
    panel = [{'vn': vn, 'wdl': 'D', 'good': i == 0, 'best': i == 0, 'result': f'máy {fmt(cp)}'}
             for i, (vn, cp) in enumerate(rows)]
    return rows, panel


def verdict_text(rows, turn):
    """Câu nhận định về thứ tự các lựa chọn, chỉ dựa trên chênh lệch điểm máy đủ lớn (>= 0,25)."""
    gaps = [abs(rows[i][1] - rows[0][1]) for i in range(1, len(rows))]
    order = '; '.join(f'{vn}, {spoken_cp(cp)}' for vn, cp in rows[:3]) + ('; các hướng còn lại kém hơn' if len(rows) > 3 else '')
    if gaps and min(gaps) >= 25:
        lead = f'Máy xếp {rows[0][0]} lên đầu, hơn hẳn các hướng còn lại'
    elif gaps and max(gaps) < 25:
        lead = 'Máy đánh giá các hướng này gần như ngang nhau, chọn hướng nào là tùy phong cách'
    else:
        lead = f'Máy xếp {rows[0][0]} lên đầu, nhưng khoảng cách với hướng sau không lớn'
    return f'{lead}. Theo thứ tự: {order}.'


def line_beat(seg, idx, ev, quiz_left):
    nodes = seg['nodes']
    first = nodes[0]
    pos0 = first['pos']
    steps = []
    if seg['branch'] is None:
        label, head = 'BIẾN CHÍNH', 'Đường đi chuẩn' if idx == 0 else 'Biến chính'
        steps.append({'say': 'Ta đi theo biến chính trước, từng nước một.'})
    else:
        kids = seg['branch']['kids']
        main_vn = vn_move(seg['branch']['pos'], seg['branch']['main'])
        alt_vn = vn_move(pos0, first['m'])
        label, head = f'BIẾN PHỤ {idx}', f'Thay vì {main_vn}: {alt_vn}'
        rows, panel_rows = ranking_rows(seg['branch']['pos'], kids, ev)
        intro = (f'Quay lại thế sau {hist(seg["prefix"])}. Biến chính đi {main_vn}, '
                 f'còn hướng ta xét bây giờ là {alt_vn}.')
        step = {'say': intro}
        if rows:
            step['say'] += ' ' + verdict_text(rows, seg['branch']['pos'].turn)
            step['rows'] = panel_rows
        steps.append(step)
    pos = pos0
    prev_cp = red_cp(ev.get(pos.fen())) if ev else None
    moves = []
    for k, n in enumerate(nodes):
        if k > 0 and len(n['kids']) > 1:
            rows, panel_rows = ranking_rows(pos, n['kids'], ev)
            names = ', '.join(vn_move(pos, m) for m in n['kids'])
            if rows and quiz_left[0] > 0 and n['ply'] >= 8 and len(n['kids']) >= 3 and n['ply'] - quiz_left[1] >= 14 and seg['branch'] is None:
                quiz_left[0] -= 1
                quiz_left[1] = n['ply']
                steps.append({'say': f'Dừng lại một chút. Ở thế này, {SIDE[pos.turn]} có {len(n["kids"])} hướng trong tư liệu: '
                                     f'{names}. Bạn sẽ chọn nước nào?', 'countdown': 5})
                steps.append({'say': verdict_text(rows, pos.turn), 'rows': panel_rows})
            elif rows:
                steps.append({'say': f'Đến đây có {len(n["kids"])} hướng: {names}. ' + verdict_text(rows, pos.turn),
                              'rows': panel_rows})
        vn = vn_move(pos, n['m'])
        parts, notes = explain(pos, n['m'], ev)
        new = pos.play(n['m'])
        cp = red_cp(ev.get(new.fen())) if ev else None
        extra = []
        if cp is not None and prev_cp is not None and abs(cp - prev_cp) >= SWING and abs(prev_cp) < 9000 and abs(cp) < 9000:
            extra.append(f'Thế cờ đổi sắc thái: từ {grade(prev_cp)} sang {grade(cp)}.')
        extra += [x + '.' for x in notes[:1]]
        say = f'{vn}.'
        if parts:
            say += ' ' + sentence(parts)
        step = {'say': f'{say} {" ".join(extra)}'.strip(), 'move': n['m'], 'ply': n['ply']}
        if cp is not None:
            step['status'] = f'Máy: {grade(cp)} ({fmt(cp)})' if abs(cp) < 9000 else f'Máy: {grade(cp)}'
        steps.append(step)
        moves.append(n['m'])
        prev_cp, pos = cp, new
    end = red_cp(ev.get(pos.fen())) if ev else None
    swaps = exchange_words(pos0, moves)
    tail = []
    if swaps:
        tail.append(f'Trong biến này có {len(swaps)} lần ăn quân: ' + '; '.join(swaps[:4]) + ('...' if len(swaps) > 4 else ''))
    if end is not None:
        tail.append(f'Kết thúc biến, {grade(end)}, máy chấm {fmt(end)}')
    if tail:
        steps.append({'say': '. '.join(tail) + '.'})
    return {'kind': 'line', 'label': label, 'headline': head, 'fen': pos0.fen(),
            'start_no': (first['ply'] + 1) // 2, 'start_side': pos0.turn, 'steps': steps}


def chapterize(beats, target):
    chapters, cur, t = [], [], 0.0
    for b in beats:
        sec = sum(est(s) for s in b['steps'])
        if cur and t + sec > target * 1.15:
            chapters.append(cur)
            cur, t = [], 0.0
        cur.append(b)
        t += sec
    if cur:
        chapters.append(cur)
    return chapters


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--opening', required=True)
    ap.add_argument('--part', type=int, default=1)
    ap.add_argument('--budget', type=int, default=230, help='số nước đi tối đa mỗi tập')
    ap.add_argument('--number', type=int, default=1)
    a = ap.parse_args()
    data = json.loads((ROOT / 'khaicuc' / 'openings' / f'{a.opening}.json').read_text(encoding='utf-8'))
    theory = json.loads((ROOT / 'khaicuc' / 'theory' / f'{a.opening}.json').read_text(encoding='utf-8'))
    ev_path = ROOT / 'khaicuc' / 'eval' / f'{a.opening}.json'
    ev = json.loads(ev_path.read_text(encoding='utf-8')) if ev_path.exists() else None
    start = Position.from_fen(data['fen'])
    segs = segments(data['tree'], start)
    # chia các đoạn thành các phần theo ngân sách số nước đi
    parts, cur, count = [], [], 0
    for s in segs:
        if cur and count + len(s['nodes']) > a.budget:
            parts.append(cur)
            cur, count = [], 0
        cur.append(s)
        count += len(s['nodes'])
    parts.append(cur)
    if not 1 <= a.part <= len(parts):
        raise SystemExit(f'Hệ này chia {len(parts)} phần, không có phần {a.part}')
    mine = parts[a.part - 1]
    base_idx = sum(len(p) for p in parts[:a.part - 1])
    beats = []
    name = theory['name']
    skip = 0
    if a.part == 1 and theory.get('intro'):
        # Phần giới thiệu: nói gọn, đi nước ngay trong lúc nói (các nước của biến chính)
        main_nodes = segs[0]['nodes']
        for blk in theory['intro']:
            steps, first_ply = [], None
            for st in blk['steps']:
                step = {'say': st['say']}
                if st.get('ply'):
                    n = main_nodes[st['ply'] - 1]
                    step.update(move=n['m'], ply=n['ply'])
                    first_ply = first_ply or n
                    skip = max(skip, st['ply'])
                    if ev:
                        cp = red_cp(ev.get(n['pos'].play(n['m']).fen()))
                        if cp is not None:
                            step['status'] = f'Máy: {grade(cp)} ({fmt(cp)})'
                steps.append(step)
            fen_node = first_ply or main_nodes[skip]
            beats.append({'kind': 'line', 'label': blk['label'], 'headline': blk['headline'], 'fen': fen_node['pos'].fen(),
                          'continue': bool(beats),
                          'start_no': (fen_node['ply'] + 1) // 2, 'start_side': fen_node['pos'].turn, 'steps': steps})
        mine[0] = dict(mine[0], nodes=main_nodes[skip:], start=main_nodes[skip]['pos'])
    elif a.part > 1:
        beats.append({'kind': 'theory', 'label': f'PHẦN {a.part}', 'headline': f'{name}: tiếp tục các biến phụ', 'fen': start.fen(),
                      'panel': {'bullets': [f'Phần {a.part}/{len(parts)}', 'Mỗi biến có điểm đánh giá của máy', 'Dừng lại tự chọn nước ở các điểm rẽ']},
                      'steps': [{'say': f'Chào mừng bạn đến phần {a.part} của chuyên đề {name}. Ta tiếp tục các biến phụ, mỗi biến đều có đánh giá của máy.'}]})
    quiz = [3, -99]
    for j, s in enumerate(mine):
        beat = line_beat(s, base_idx + j, ev, quiz)
        beat['continue'] = bool(a.part == 1 and j == 0 and theory.get('intro'))
        beats.append(beat)
    beats.append({'kind': 'mnemonic', 'label': 'KHẨU QUYẾT', 'headline': name, 'panel': {'bullets': theory['mnemonic']},
                  'steps': [{'say': 'Khẩu quyết cho bài này. ' + ' '.join(theory['mnemonic'])},
                            {'say': theory['closing']}]})
    beats.append({'kind': 'cta', 'label': 'CẢM ƠN BẠN', 'headline': 'Đăng ký kênh và ủng hộ ly cà phê',
                  'steps': [{'say': theory['cta']}]})
    chapters = chapterize(beats, CHAPTER_SECONDS)
    total = sum(est(s) for b in beats for s in b['steps'])
    ep_id = f'kc-{a.number:04d}'
    title = f'Khai cục {name} – phần {a.part}: {theory["tagline"]}'
    series_tag = f'[Khai cục chuyên sâu #{a.number}]'
    out = {'id': ep_id, 'number': a.number, 'opening': a.opening, 'part': a.part, 'parts': len(parts),
           'title': title, 'subtitle': theory['tagline'], 'category': 'Khai cục', 'fen': start.fen(),
           'card_note': 'Phân tích kèm điểm đánh giá của Pikafish',
           'outro_title': 'ĐĂNG KÝ KÊNH ĐỂ KHÔNG BỎ LỠ!',
           'outro_text': 'Series khai cục chuyên sâu ra đều đặn. Bấm đăng ký để nhận phần tiếp theo. Thấy hay thì ủng hộ kênh một ly cà phê nhé! ☕',
           'chapters': [{'title': c[0]['headline'], 'beats': c} for c in chapters],
           'est_minutes': round(total / 60, 1),
           'youtube': {'title': f'{series_tag} {title}',
                       'tags': ['cờ tướng', 'khai cục', 'khai cục cờ tướng', name.lower(), 'phân tích khai cục', 'cờ tướng chuyên sâu',
                                'series khai cục chuyên sâu', 'xiangqi', 'chinese chess opening', 'tinh hoa cờ tàn', 'học cờ tướng']}}
    dest = ROOT / 'khaicuc' / 'episodes'
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f'{ep_id}.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'{ep_id}: phần {a.part}/{len(parts)}, {len(mine)} đoạn biến, {sum(len(s["nodes"]) for s in mine)} nước, '
          f'{len(chapters)} chương, ước tính {total / 60:.0f} phút')


if __name__ == '__main__':
    main()
