#!/usr/bin/env python3
"""Dựng tập 'bẫy khai cục' (nhiều thế bẫy ngắn gộp thành một video dài) từ khaicuc/openings/bay-*.json.

python scripts/build_khaicuc_traps.py --group 1 --size 4 --number 90
Mỗi thế bẫy: giới thiệu, diễn biến (biến chính), vài biến phụ, câu đố ở nước 'tung đòn' (nước có điểm máy
tăng mạnh nhất cho bên đi), kết quả theo điểm máy. Cuối tập: khẩu quyết + kêu gọi đăng ký/ủng hộ.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_khaicuc_episode as B  # noqa: E402
from xq.board import Position  # noqa: E402
from xq.notation import vn_move  # noqa: E402
from xq.opening_commentary import SIDE, red_cp, spoken_cp  # noqa: E402

MAX_ALTS = 2


def trap_slugs():
    out = []
    for f in sorted((ROOT / 'khaicuc' / 'openings').glob('bay-*.json')):
        d = json.loads(f.read_text(encoding='utf-8'))
        if d['stats']['nodes'] > 0:
            out.append(d['slug'])
    return out


def springing_ply(nodes, ev):
    """Nút có bên đi hưởng lợi nhiều nhất theo điểm máy (>= 1,2 điểm) -> ply, hoặc None."""
    best, ply = 120, None
    for n in nodes:
        a, b = red_cp(ev.get(n['pos'].fen())), red_cp(ev.get(n['pos'].play(n['m']).fen()))
        if a is None or b is None:
            continue
        gain = (b - a) * (1 if n['pos'].turn == 'w' else -1)
        if gain > best and abs(a) < 9000:
            best, ply = gain, n['ply']
    return ply


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--group', type=int, required=True)
    ap.add_argument('--size', type=int, default=6)
    ap.add_argument('--number', type=int, required=True)
    a = ap.parse_args()
    slugs = trap_slugs()
    groups = [slugs[i:i + a.size] for i in range(0, len(slugs), a.size)]
    if not 1 <= a.group <= len(groups):
        raise SystemExit(f'Có {len(groups)} nhóm bẫy, không có nhóm {a.group}')
    mine = groups[a.group - 1]
    meta = json.loads((ROOT / 'khaicuc' / 'meta.json').read_text(encoding='utf-8'))
    fam = meta['families']['trap']
    cta = json.loads((ROOT / 'khaicuc' / 'theory' / 'thuanphao.json').read_text(encoding='utf-8'))['cta']
    beats, names, first_fen = [], [], None
    for k, slug in enumerate(mine, 1):
        d = json.loads((ROOT / 'khaicuc' / 'openings' / f'{slug}.json').read_text(encoding='utf-8'))
        ev_path = ROOT / 'khaicuc' / 'eval' / f'{slug}.json'
        ev = json.loads(ev_path.read_text(encoding='utf-8')) if ev_path.exists() else {}
        start = Position.from_fen(d['fen'])
        first_fen = first_fen or start.fen()
        segs = B.segments(d['tree'], start)
        name = d['title_vi']
        names.append(name)
        if k == 1:
            beats.append({'kind': 'theory', 'label': 'MỞ ĐẦU', 'headline': 'Bẫy khai cục: một nước lơ là là mất quân',
                          'fen': start.fen(), 'panel': {'bullets': [f'{len(mine)} thế bẫy trong tập này', 'Mỗi bẫy có điểm đánh giá của máy',
                                                                   'Có câu đố: bạn thấy bẫy trước không?']},
                          'steps': [{'say': f'Khai cục có những cái bẫy chỉ cần một nước lơ là là mất quân. Trong tập này ta xem {len(mine)} thế bẫy, '
                                            'từng nước một, và xem máy đánh giá khoảnh khắc đòn bẫy được tung ra.'}]})
        beats.append({'kind': 'theory', 'label': f'BẪY {k}/{len(mine)}', 'headline': name, 'fen': start.fen(),
                      'panel': {'bullets': [name, f'{sum(len(s["nodes"]) for s in segs)} nước đi trong tư liệu']},
                      'steps': [{'say': f'Bẫy số {k}. {name}. Hãy theo dõi nước đi hấp dẫn của đối phương, vì có thể đó chính là mồi nhử.'}]})
        quiz = [0, -99]
        main = B.line_beat(segs[0], 0, ev, quiz)
        sp = springing_ply(segs[0]['nodes'], ev) if ev else None
        if sp:
            steps = main['steps']
            i = next((j for j, s in enumerate(steps) if s.get('ply') == sp), None)
            if i is not None:
                node = next(n for n in segs[0]['nodes'] if n['ply'] == sp)
                after = red_cp(ev.get(node['pos'].play(node['m']).fen()))
                steps.insert(i, {'say': f'Dừng lại một chút. Đến lượt {SIDE[node["pos"].turn]}, có một nước đi rất mạnh. Bạn tìm ra không?',
                                 'countdown': 5})
                steps[i + 1]['say'] += f' Đây chính là đòn quyết định: máy chấm {spoken_cp(after)}.'
        main['label'], main['headline'] = f'BẪY {k} · DIỄN BIẾN', 'Diễn biến chính'
        beats.append(main)
        for j, s in enumerate(segs[1:1 + MAX_ALTS], 1):
            b = B.line_beat(s, j, ev, quiz)
            b['label'] = f'BẪY {k} · BIẾN PHỤ {j}'
            beats.append(b)
    beats.append({'kind': 'mnemonic', 'label': 'KHẨU QUYẾT', 'headline': 'Tránh bẫy khai cục', 'panel': {'bullets': fam['mnemonic']},
                  'steps': [{'say': 'Khẩu quyết để tránh bẫy. ' + ' '.join(fam['mnemonic'])}, {'say': fam['closing']}]})
    beats.append({'kind': 'cta', 'label': 'CẢM ƠN BẠN', 'headline': 'Đăng ký kênh và ủng hộ ly cà phê', 'steps': [{'say': cta}]})
    chapters = B.chapterize(beats, B.CHAPTER_SECONDS)
    total = sum(B.est(s) for b in beats for s in b['steps'])
    ep_id = f'kc-{a.number:04d}'
    title = f'Bẫy khai cục – tuyển tập {a.group}: {len(mine)} thế bẫy bạn cần biết'
    out = {'id': ep_id, 'number': a.number, 'opening': f'bay-nhom-{a.group}', 'part': a.group, 'parts': len(groups), 'title': title,
           'subtitle': 'Bẫy khai cục', 'category': 'Khai cục', 'fen': first_fen,
           'card_note': 'Phân tích kèm điểm đánh giá của Pikafish',
           'outro_title': 'ĐĂNG KÝ KÊNH ĐỂ KHÔNG BỎ LỠ!',
           'outro_text': 'Series khai cục chuyên sâu ra đều đặn. Bấm đăng ký để nhận phần tiếp theo. Thấy hay thì ủng hộ kênh một ly cà phê nhé! ☕',
           'chapters': [{'title': c[0]['headline'], 'beats': c} for c in chapters], 'est_minutes': round(total / 60, 1),
           'traps': names,
           'youtube': {'title': f'[Khai cục chuyên sâu #{a.number}] {title}',
                       'tags': ['cờ tướng', 'khai cục', 'bẫy khai cục', 'bẫy cờ tướng', 'phân tích khai cục', 'cờ tướng chuyên sâu',
                                'series khai cục chuyên sâu', 'xiangqi', 'chinese chess traps', 'tinh hoa cờ tàn', 'học cờ tướng']}}
    dest = ROOT / 'khaicuc' / 'episodes'
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f'{ep_id}.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'{ep_id}: nhóm bẫy {a.group}/{len(groups)}, {len(mine)} thế, {len(chapters)} chương, ước tính {total / 60:.0f} phút')


if __name__ == '__main__':
    main()
