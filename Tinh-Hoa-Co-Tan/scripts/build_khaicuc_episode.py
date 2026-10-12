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
from xq.opening_commentary import SIDE, explain, grade, red_cp, sentence  # noqa: E402

WPS = 3.9            # từ/giây của giọng đọc (Thiện Minh ~4,2)
STEP_PAD = 1.5       # giây hoạt ảnh mỗi nước
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
            nodes.append({'m': c['m'], 'ply': c['ply'], 'pos': p})
            p = p.play(c['m'])
            cur = c
        out.append({'prefix': list(prefix), 'branch': branch_from, 'start': pos, 'nodes': nodes})
        # biến phụ: từ nút sâu nhất ngược lên
        for idx, alt, bpos, main_kid in reversed(alts):
            pref = prefix + [(n['ply'], n['pos'], n['m']) for n in nodes[:idx]]
            # alt là nút con thay thế: đoạn mới bắt đầu bằng chính nó
            wrapper = {'c': [alt]}
            chain(wrapper, bpos, pref, {'main': main_kid['m'], 'pos': bpos})

    chain(tree, start, [], None)
    return out


def words(text):
    return len(re.findall(r'\w+', text))


def est(step):
    return words(step['say']) / WPS + (STEP_PAD if step.get('move') else 0.4) + step.get('countdown', 0)


def hist(prefix):
    """'5. Xe 1 bình 2' của nước cuối trước điểm rẽ."""
    if not prefix:
        return None
    ply, pos, m = prefix[-1]
    return f'nước {(ply + 1) // 2}, {SIDE[pos.turn]} đi {vn_move(pos, m)}'


def line_beat(seg, idx, ev, quiz_left):
    nodes = seg['nodes']
    first = nodes[0]
    pos0 = first['pos']
    steps, last_cp = [], None
    if seg['branch'] is None:
        label, head = 'BIẾN CHÍNH', 'Đường đi chuẩn của Thuận Pháo' if idx == 0 else 'Biến chính'
        intro = 'Ta bắt đầu với biến chính, từng nước một.'
    else:
        main_vn = vn_move(seg['branch']['pos'], seg['branch']['main'])
        alt_vn = vn_move(pos0, first['m'])
        label = f'BIẾN PHỤ {idx}'
        head = f'Thay vì {main_vn}: {alt_vn}'
        where = hist(seg['prefix'])
        intro = (f'Quay lại thế sau {where}. Ở đây biến chính đi {main_vn}, '
                 f'nhưng {SIDE[pos0.turn]} còn một lựa chọn khác là {alt_vn}.')
    steps.append({'say': intro})
    pos = pos0
    prev_cp = red_cp(ev.get(pos.fen())) if ev else None
    for k, n in enumerate(nodes):
        vn = vn_move(pos, n['m'])
        parts, notes = explain(pos, n['m'], ev)
        s = sentence(parts)
        new = pos.play(n['m'])
        cp = red_cp(ev.get(new.fen())) if ev else None
        extra = []
        if cp is not None and prev_cp is not None and abs(cp - prev_cp) >= SWING and abs(prev_cp) < 9000:
            extra.append(f'Đây là bước ngoặt: {grade(cp)}.')
        if notes and (k < 2 or extra or 'tốt hơn khoảng' in notes[0]):
            extra.append(notes[0] + '.')
        step = {'say': f'{vn}. {s} {" ".join(extra)}'.strip(), 'move': n['m'], 'ply': n['ply']}
        if cp is not None:
            step['status'] = f'Máy: {grade(cp)} ({cp / 100:+.2f})' if abs(cp) < 9000 else f'Máy: {grade(cp)}'
        if quiz_left[0] > 0 and k == 0 and seg['branch'] is None and False:
            pass
        steps.append(step)
        prev_cp, pos = cp, new
    end = red_cp(ev.get(pos.fen())) if ev else None
    if end is not None:
        steps.append({'say': f'Kết thúc biến này: {grade(end)}.'})
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
    ap.add_argument('--budget', type=int, default=300, help='số nước đi tối đa mỗi tập')
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
    if a.part == 1:
        beats.append({'kind': 'hook', 'label': 'MỞ ĐẦU', 'headline': f'{name}: {theory["tagline"]}', 'fen': start.fen(),
                      'panel': {'bullets': [theory['tagline'], f'{len(segs)} đường biến trong tư liệu',
                                            f'{sum(len(s["nodes"]) for s in segs)} nước đi được phân tích']},
                      'steps': [{'say': theory['hook']},
                                {'say': f'Trong video này ta phân tích {name} từng nước một, có điểm đánh giá của máy Pikafish, '
                                        'ý đồ của mỗi bên và khẩu quyết dễ nhớ ở cuối bài.'},
                                {'say': 'Một lưu ý trước khi bắt đầu. Vì Đỏ đi trước, máy thường cho Đỏ hơn khoảng ba đến năm phần mười điểm '
                                        'ngay từ đầu. Đó là lợi thế của người đi trước, không có nghĩa là Đen đã đi sai.'}]})
        for i, idea in enumerate(theory['ideas'], 1):
            beats.append({'kind': 'theory', 'label': f'Ý TƯỞNG {i}', 'headline': idea['title'], 'fen': start.fen(),
                          'panel': {'bullets': idea['bullets']}, 'steps': [{'say': idea['say']}]})
    quiz = [3]
    for j, s in enumerate(mine):
        beats.append(line_beat(s, base_idx + j, ev, quiz))
    beats.append({'kind': 'mnemonic', 'label': 'KHẨU QUYẾT', 'headline': name, 'panel': {'bullets': theory['mnemonic']},
                  'steps': [{'say': 'Khẩu quyết cho bài này. ' + ' '.join(theory['mnemonic'])},
                            {'say': theory['closing'] + ' Hẹn gặp lại bạn ở phần tiếp theo của chuyên đề khai cục.'}]})
    chapters = chapterize(beats, CHAPTER_SECONDS)
    total = sum(est(s) for b in beats for s in b['steps'])
    ep_id = f'kc-{a.number:04d}'
    title = f'Khai cục {name} – phần {a.part}: {theory["tagline"]}'
    out = {'id': ep_id, 'number': a.number, 'opening': a.opening, 'part': a.part, 'parts': len(parts),
           'title': title, 'subtitle': theory['tagline'], 'category': 'Khai cục', 'fen': start.fen(),
           'card_note': 'Phân tích kèm điểm đánh giá của Pikafish',
           'chapters': [{'title': c[0]['headline'], 'beats': c} for c in chapters],
           'est_minutes': round(total / 60, 1),
           'youtube': {'title': f'{title} | Tinh Hoa Cờ Tàn',
                       'tags': ['cờ tướng', 'khai cục', name.lower(), 'phân tích khai cục', 'tinh hoa cờ tàn']}}
    dest = ROOT / 'khaicuc' / 'episodes'
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f'{ep_id}.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'{ep_id}: phần {a.part}/{len(parts)}, {len(mine)} đoạn biến, {sum(len(s["nodes"]) for s in mine)} nước, '
          f'{len(chapters)} chương, ước tính {total / 60:.0f} phút')


if __name__ == '__main__':
    main()
