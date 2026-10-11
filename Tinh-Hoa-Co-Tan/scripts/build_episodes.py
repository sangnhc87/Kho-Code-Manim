#!/usr/bin/env python3
"""Dựng kịch bản tập mới từ giáo trình, dữ liệu lấy từ bảng tra chessdb.cn.

    python scripts/build_episodes.py --count 3            # 3 tập kế tiếp theo giáo trình
    python scripts/build_episodes.py --topic ma-si --count 1
    python scripts/build_episodes.py --fen "<FEN>" --topic ma-si   # thế chọn tay

Mỗi tập ghi ra episodes/ep-XXXX.json (kịch bản + phân tích đầy đủ), catalog.json
giữ danh mục và khoá chống trùng (thế cờ và ảnh gương coi là một).
"""
import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from xq import cdb  # noqa: E402
from xq.analyze import analyze  # noqa: E402
from xq.board import RED, Position, side_of  # noqa: E402
from xq.commentary import build_episode, moves_count  # noqa: E402
from xq.sample import canonical, random_position  # noqa: E402

CURRICULUM = ROOT / 'curriculum' / 'topics.json'
CATALOG = ROOT / 'catalog.json'
EPISODES = ROOT / 'episodes'


def load_json(path, default):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else default


def hanging(pos):
    """Có quân Đỏ (trừ Tướng) đang bị ăn mà không được bảo vệ không?"""
    for sq, p in pos.cells.items():
        if side_of(p) != RED or p == 'K':
            continue
        attacked = any(side_of(q) != RED and pos.attacks(s, sq) for s, q in pos.cells.items())
        if not attacked:
            continue
        probe = Position(pos.cells, RED)
        probe.cells[sq] = 'p'  # giả sử bị ăn: quân Đỏ nào ăn lại được ô này?
        if not any(side_of(q) == RED and probe.attacks(s, sq) for s, q in probe.cells.items()):
            return True
    return False


def quick_filter(pos, topic):
    res = cdb.query(pos.fen())
    if res['status'] != 'egtb':
        return None
    moves = res['moves']
    best = moves[0]
    want = topic.get('result', 'W')
    if best['wdl'] != want:
        return None
    lo, hi = topic.get('dtm', [15, 45])
    if want == 'W' and not lo <= best['dtm'] <= hi:
        return None
    wins = sum(m['wdl'] == want for m in moves)
    fastest = sum(m['wdl'] == want and m['dtm'] == best['dtm'] for m in moves)
    if wins == len(moves):
        return None  # câu đố phải có lựa chọn sai thật sự
    if wins > topic.get('max_first_keep', 3) and fastest > 1:
        return None  # nhiều nước thắng: chỉ nhận khi có đúng một nước thắng nhanh nhất
    first = best['move']
    if first[2:] and pos.cells.get((ord(first[2]) - 97, int(first[3]))) and not topic.get('allow_first_capture'):
        return None
    return {'wins': wins, 'dtm': best['dtm']}


def score(a):
    att = a['attacker']
    main = a['main']
    onlys = sum(1 for p in main if p['side'] == att and p['only'])
    waits = sum(1 for p in main if p.get('zug', {}).get('type') == 'waiting' and p['zug']['key'])
    zugs = sum(1 for p in main if p.get('zug', {}).get('type') == 'zugzwang')
    first_only = 1 if main and main[0]['only'] else 0
    return (4 * first_only + 2 * min(onlys, 4) + 3 * min(waits, 2) + 3 * min(zugs, 2)
            + 2 * len(a['traps']) + min(a['value']['dtm'], 50) / 12)


def find_position(topic, used, rng, samples, finalists):
    red, black = topic['material']
    constraints = {k: [tuple(s) for s in v] for k, v in topic.get('constraints', {}).items()}
    pool = []
    for _ in range(samples):
        pos = random_position(red, black, turn=RED, rng=rng, constraints=constraints)
        key = canonical(pos.fen())
        if key in used or pos.in_check(RED) or hanging(pos):
            continue
        try:
            q = quick_filter(pos, topic)
        except cdb.CdbError as exc:
            print('  bỏ qua', exc)
            continue
        if q:
            pool.append((q['wins'], -q['dtm'], pos.fen()))
            used_now = key
            used = used | {used_now}
    cdb.flush()
    if not pool:
        raise SystemExit(f'Không tìm được thế phù hợp cho chủ đề {topic["id"]}; tăng --samples.')
    pool.sort()
    best, best_score = None, -1
    for _, _, fen in pool[:finalists]:
        a = analyze(fen)
        s = score(a)
        print(f'  ứng viên {fen}  điểm {s:.1f}  bí {a["value"]["dtm"]}  bẫy {len(a["traps"])}')
        if s > best_score:
            best, best_score = a, s
        cdb.flush()
    return best


def youtube_meta(ep, topic, a, title):
    lines = []
    main = a['main']
    for i in range(0, len(main), 2):
        red = main[i]['vn']
        black = main[i + 1]['vn'] if i + 1 < len(main) else ''
        lines.append(f'{i // 2 + 1}. {red}   {black}'.rstrip())
    val = a['value']
    verdict = (f'Đỏ đi trước thắng, chiếu bí sau {moves_count(val["dtm"])} nước' if val['wdl'] == 'W'
               else 'Hòa nếu Đen phòng thủ chính xác')
    desc = f"""{title}

{topic['short']} — {verdict} (theo bảng tra cờ tàn chessdb.cn, hai bên chơi tối ưu).

Thế cờ (FEN): {a['fen']}

Biến chính:
{chr(10).join(lines)}

Chuyên đề: {topic['category']}. Kiến thức nền: {topic['takeaway']}

Mọi kết luận thắng/hòa và số nước đều được tra từ bảng tra cờ tàn (endgame tablebase) của Cơ sở dữ liệu đám mây chessdb.cn.

☕ Ủng hộ kênh một ly cà phê: VPBank 10389821115 (Quét VietQR cuối video).

#CoTuong #CoTan #TinhHoaCoTan #{topic['category'].replace(' ', '')}"""
    tags = ['cờ tướng', 'cờ tàn', 'tinh hoa cờ tàn', 'học cờ tướng', topic['category'].lower(),
            topic['short'].lower(), 'xiangqi', 'endgame']
    return {'title': f'{title} | Tinh Hoa Cờ Tàn #{ep}', 'description': desc, 'tags': tags,
            'playlist': f'Tinh Hoa Cờ Tàn | {topic["category"]}'}


def episode_hooks(a):
    """Các điểm nhấn của thế cờ, theo thứ tự ưu tiên."""
    main, att = a['main'], a['attacker']
    hooks = []
    if main and main[0]['only']:
        hooks.append('Nước thắng duy nhất')
    if any(p.get('zug', {}).get('type') == 'waiting' and p['zug']['key'] for p in main):
        hooks.append('Nước chờ quyết định')
    if any(p.get('zug', {}).get('type') == 'zugzwang' for p in main):
        hooks.append('Đòn ép nước')
    kinds = {t['lure']['kind'] for t in a['traps']}
    if any(t['lure']['piece'] == 'P' and t['lure']['move'][3] == '9' for t in a['traps']):
        hooks.append('Đừng vội xuống đáy')
    if 'check' in kinds:
        hooks.append('Nước chiếu sai lầm')
    if 'capture' in kinds:
        hooks.append('Miếng mồi độc')
    if sum(1 for p in main if p['side'] == att and p['only']) >= 2:
        hooks.append('Từng nước phải chính xác')
    if a['mate'] and not a['mate']['in_check']:
        hooks.append('Thắng bằng hết nước')
    hooks.append('Kỹ thuật ép cung')
    return hooks


def episode_title(topic, a, variant_no, used_titles=()):
    hooks = episode_hooks(a)
    hook = next((h for h in hooks if not any(h in t for t in used_titles)), hooks[0])
    return f'{topic["title"]} – Thế {variant_no}: {hook}'


def build(topic, ep, fen=None, rng=None, samples=400, finalists=6, catalog=None):
    used = {e['key'] for e in catalog['episodes']}
    if fen:
        a = analyze(Position.from_fen(fen).fen())
    else:
        a = find_position(topic, used, rng, samples, finalists)
    variant = 1 + sum(1 for e in catalog['episodes'] if e['topic'] == topic['id'])
    title = episode_title(topic, a, variant,
                          [e['title'] for e in catalog['episodes'] if e['topic'] == topic['id']])
    beats = build_episode(a, topic, ep)
    data = {
        'id': f'ep-{ep:04d}', 'number': ep, 'topic': topic['id'], 'category': topic['category'],
        'title': title, 'subtitle': topic['short'], 'fen': a['fen'],
        'verdict': a['value'], 'source': 'chessdb.cn EGTB (DTM)',
        'beats': beats, 'youtube': youtube_meta(ep, topic, a, title), 'analysis': a,
    }
    EPISODES.mkdir(exist_ok=True)
    (EPISODES / f'ep-{ep:04d}.json').write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n',
                                               encoding='utf-8')
    catalog['episodes'].append({'ep': ep, 'topic': topic['id'], 'fen': a['fen'],
                                'key': canonical(a['fen']), 'title': title})
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    cdb.flush()
    print(f'ep-{ep:04d}: {title}  ({len(beats)} phân đoạn)')
    return data


def next_topics(topics, catalog, count):
    done = {}
    for e in catalog['episodes']:
        done[e['topic']] = done.get(e['topic'], 0) + 1
    out = []
    for t in topics:
        left = t.get('episodes', 1) - done.get(t['id'], 0)
        out += [t] * max(0, left)
    return out[:count]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--count', type=int, default=1)
    ap.add_argument('--topic')
    ap.add_argument('--fen')
    ap.add_argument('--samples', type=int, default=400)
    ap.add_argument('--finalists', type=int, default=6)
    ap.add_argument('--seed', type=int)
    args = ap.parse_args()
    topics = load_json(CURRICULUM, {})['topics']
    by_id = {t['id']: t for t in topics}
    catalog = load_json(CATALOG, {'episodes': []})
    if args.topic:
        plan = [by_id[args.topic]] * args.count
    else:
        plan = next_topics(topics, catalog, args.count)
    if not args.topic:
        plan = next_topics(topics, catalog, 10 ** 6)
    built, failed = 0, set()
    for topic in plan:
        if built >= args.count:
            break
        if topic['id'] in failed:
            continue
        ep = 1 + max([e['ep'] for e in catalog['episodes']] or [0])
        rng = random.Random(args.seed if args.seed is not None else ep * 7919)
        try:
            build(topic, ep, fen=args.fen, rng=rng, samples=args.samples, finalists=args.finalists,
                  catalog=catalog)
            built += 1
        except (SystemExit, cdb.CdbError) as exc:
            print(f'CẢNH BÁO: bỏ qua chủ đề {topic["id"]}: {exc}')
            failed.add(topic['id'])
            cdb.flush()
    if built < args.count:
        raise SystemExit(f'Chỉ dựng được {built}/{args.count} tập')


if __name__ == '__main__':
    main()
