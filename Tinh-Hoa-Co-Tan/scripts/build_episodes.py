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
    if want == 'D':
        # Thủ hòa: Đen đi trước, chỉ vài nước giữ hòa, còn lại đều thua.
        holds = sum(m['wdl'] == 'D' for m in moves)
        if holds > topic.get('max_first_keep', 2) or holds == len(moves) or len(moves) < 4:
            return None
        return {'wins': holds, 'dtm': -max(m['dtm'] for m in moves if m['wdl'] == 'L')}
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
    if a['value']['wdl'] == 'D':
        holds = sum(1 for p in main if p['side'] != att and p['only'])
        return 3 * min(holds, 5) + 2 * len(a['traps']) + (3 if main and main[0]['only'] else 0)
    onlys = sum(1 for p in main if p['side'] == att and p['only'])
    waits = sum(1 for p in main if p.get('zug', {}).get('type') == 'waiting' and p['zug']['key'])
    zugs = sum(1 for p in main if p.get('zug', {}).get('type') == 'zugzwang')
    first_only = 1 if main and main[0]['only'] else 0
    return (4 * first_only + 2 * min(onlys, 4) + 3 * min(waits, 2) + 3 * min(zugs, 2)
            + 2 * len(a['traps']) + min(a['value']['dtm'], 50) / 12)


def level(topic, variant):
    """Thế thứ n của chủ đề khó dần: chia dải DTM thành 3 bậc, đi từ ngắn đến dài."""
    if topic.get('result') == 'D' or 'dtm' not in topic:
        return topic
    lo, hi = topic['dtm']
    n = 3
    width = max(2, (hi - lo) // n)
    i = (variant - 1) % n
    band = [lo + i * width, hi if i == n - 1 else lo + (i + 1) * width + 2]
    return {**topic, 'dtm': band, '_full_band': [lo, hi]}


def find_position(topic, used, rng, samples, finalists):
    red, black = topic['material']
    constraints = {k: [tuple(s) for s in v] for k, v in topic.get('constraints', {}).items()}
    pool = []
    for _ in range(samples):
        turn = 'b' if topic.get('result') == 'D' else RED
        pos = random_position(red, black, turn=turn, rng=rng, constraints=constraints)
        key = canonical(pos.fen())
        if key in used or pos.in_check(pos.turn) or (turn == RED and hanging(pos)):
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
    if not pool and topic.get('_full_band'):
        return find_position({**topic, 'dtm': topic['_full_band'], '_full_band': None}, used, rng, samples, finalists)
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
    if a['value']['wdl'] == 'D':
        if main and main[0]['only']:
            hooks.append('Nước giữ hòa duy nhất')
        if a['traps']:
            hooks.append('Một nước sai là thua')
        if sum(1 for p in main if p['side'] != att and p['only']) >= 2:
            hooks.append('Phòng thủ từng nước')
        hooks.append('Nghệ thuật thủ hòa')
        return hooks
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
    variant = 1 + sum(1 for e in catalog['episodes'] if e['topic'] == topic['id'])
    if fen:
        a = analyze(Position.from_fen(fen).fen())
    else:
        a = find_position(level(topic, variant), used, rng, samples, finalists)
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


def next_classics(collection, catalog, min_pieces=0, include_brief=False):
    """Các thế chưa dựng của một cuốn sách, theo đúng thứ tự trong sách, chỉ lấy thế có bảng tra."""
    data = load_json(ROOT / 'curriculum' / 'classics' / f'{collection}.json', {'items': {}})
    done = {e.get('source_file') for e in catalog['episodes']}
    used = {e['key'] for e in catalog['episodes']}
    out = []
    for f, item in data['items'].items():
        if f in done or item['tb'].get('status') != 'egtb' or canonical(item['fen']) in used:
            continue
        if not include_brief and item['tb']['wdl'] == 'W' and item['tb']['dtm'] < 5:
            continue  # chiếu bí 1-2 nước: không đủ nội dung cho một tập dài
        if item.get('pieces', 99) < min_pieces:
            continue
        out.append((f, item))
    return out


def build_classic(collection, file_name, item, ep, topics, catalog):
    from xq.classics import classic_topic
    a = analyze(item['fen'], prefer=item.get('book_moves'))
    topic = classic_topic(collection, file_name, item, a, topics)
    hooks = episode_hooks(a)
    title = f'{topic["title"]}: {hooks[0]}'
    beats = build_episode(a, topic, ep)
    meta = youtube_meta(ep, topic, a, title)
    book = topic['book']
    meta['description'] = meta['description'].replace(
        'Mọi kết luận thắng/hòa',
        f'Thế cờ số {topic["book_number"]} trong sách "{book["name"]}"'
        + (f' ({book["author"]})' if book['author'] else '') +
        '; dữ liệu kỳ phổ từ kho cộng đồng vietcotuong.com.\n\nMọi kết luận thắng/hòa')
    meta['playlist'] = f'Tinh Hoa Cờ Tàn | {book["name"]}'
    data = {
        'id': f'ep-{ep:04d}', 'number': ep, 'topic': topic['id'], 'category': topic['category'],
        'title': title, 'subtitle': topic['short'], 'fen': a['fen'], 'verdict': a['value'],
        'source': 'chessdb.cn EGTB (DTM)', 'classic': {'collection': collection, 'file': file_name,
                                                       'book_result': item.get('book_result'),
                                                       'book_moves': item.get('book_moves', [])},
        'topic_data': topic, 'beats': beats, 'youtube': meta, 'analysis': a,
    }
    if collection == 'Co-Tan-Thuc-Dung':
        import importlib.util
        spec = importlib.util.spec_from_file_location('make_short', ROOT / 'scripts' / 'make_short.py')
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        data['youtube_short'] = mod.reel_copy(data)
    (EPISODES / f'ep-{ep:04d}.json').write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n',
                                               encoding='utf-8')
    catalog['episodes'].append({'ep': ep, 'topic': topic['id'], 'fen': a['fen'], 'key': canonical(a['fen']),
                                'title': title, 'source_file': file_name})
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    cdb.flush()
    print(f'ep-{ep:04d}: {title}  ({len(beats)} phân đoạn)')
    return data


GAME_BOOKS = {'Dai-Su-Ky-Lo-Ho-Vinh-Hoa': 'Đại sư kỳ lộ Hồ Vinh Hoa'}


def next_games(collection, catalog, min_plies=10):
    """Ván có tàn cuộc đáng xem nhất trước: nhiều sai lầm / nước duy nhất."""
    data = load_json(ROOT / 'curriculum' / 'games' / f'{collection}.json', {'games': {}})
    done = {e.get('source_file') for e in catalog['episodes']}
    good = []
    for f, g in data['games'].items():
        es = g.get('endgame')
        if f in done or not es or len(es['plies']) < min_plies:
            continue
        if es['errors'] == 0 and es['only_found'] < 2:
            continue
        good.append((-(2 * es['errors'] + es['only_found']), f, g))
    return [(f, g) for _, f, g in sorted(good)]


def build_game(collection, file_name, game, ep, catalog):
    from xq.game_episode import build_game_episode
    beats, info = build_game_episode(game, GAME_BOOKS.get(collection, collection), ep)
    es = game['endgame']
    names = ' – '.join(n for n in (info['red'], info['black']) if not n.startswith('kỳ thủ')) or 'Danh thủ'
    hook = 'Sai lầm ở tàn cuộc' if info['errors'] else 'Nước duy nhất của danh thủ'
    who = ' – '.join(n for n in (info['red'], info['black']) if not n.startswith('kỳ thủ'))
    short_title = ((f'Danh thủ cũng đi sai! Bạn tìm ra nước đúng? ' if info['errors'] else
                    'Chỉ một nước đúng – danh thủ có tìm ra? ')
                   + (f'({who}{", " + info["year"] if info["year"] else ""}) ' if who else '') + '#Shorts')
    title = f'Thực chiến: {names}' + (f' ({info["year"]})' if info['year'] else '') + f': {hook}'
    desc = (f'{title}\n\nTàn cuộc trong ván đấu thật'
            + (f' năm {info["year"]}' if info['year'] else '') +
            f', được bảng tra cờ tàn chessdb.cn chấm chính xác từng nước.\n'
            f'Bảng tra: {info["verdict"]} • Ván thật: {info["real"]} • {info["errors"]} sai lầm • '
            f'{info["finds"]} nước duy nhất.\n\nThế vào tàn cuộc (FEN): {es["entry_fen"]}\n'
            f'Kỳ phổ: {GAME_BOOKS.get(collection, collection)} (kho cộng đồng vietcotuong.com).\n\n'
            '☕ Ủng hộ kênh một ly cà phê: VPBank 10389821115 (Quét VietQR cuối video).\n\n'
            '#CoTuong #CoTan #TinhHoaCoTan #ThucChien')
    data = {
        'id': f'ep-{ep:04d}', 'number': ep, 'kind': 'game', 'topic': f'game-{collection}',
        'category': 'Thực chiến danh thủ', 'title': title, 'subtitle': 'Tàn cuộc thực chiến',
        'fen': es['entry_fen'], 'verdict': {'wdl': es['entry_value'], 'dtm': es['entry_dtm']},
        'base_status': 'Bảng tra chessdb', 'source': 'chessdb.cn EGTB (DTM)',
        'game': {k: game[k] for k in ('red', 'black', 'event', 'date', 'result', 'title')},
        'beats': beats, 'analysis': None,
        'youtube_short': {'title': short_title, 'description': desc.replace('#ThucChien', '#ThucChien #Shorts')},
        'youtube': {'title': f'{title} | Tinh Hoa Cờ Tàn #{ep}', 'description': desc,
                    'tags': ['cờ tướng', 'cờ tàn', 'thực chiến', 'danh thủ', 'tinh hoa cờ tàn', 'xiangqi'],
                    'playlist': 'Tinh Hoa Cờ Tàn | Thực chiến danh thủ'},
    }
    from xq.validate import validate_episode
    validate_episode(data)
    (EPISODES / f'ep-{ep:04d}.json').write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n',
                                               encoding='utf-8')
    catalog['episodes'].append({'ep': ep, 'topic': data['topic'], 'fen': es['entry_fen'],
                                'key': canonical(es['entry_fen']), 'title': title, 'source_file': file_name})
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'ep-{ep:04d}: {title}  ({len(beats)} phân đoạn)')
    return data


PIECE_VN = {'R': 'Xe', 'N': 'Mã', 'C': 'Pháo', 'P': 'Binh', 'A': 'Sĩ', 'B': 'Tượng'}


def sac_phrase(sacs):
    """['R','R','C'] -> 'thí 2 Xe và Pháo'."""
    if not sacs:
        return ''
    parts = []
    for u in 'RNCPAB':
        k = sacs.count(u)
        if k:
            parts.append(f'{k} {PIECE_VN[u]}' if k > 1 else PIECE_VN[u])
    return 'thí ' + (' và '.join([', '.join(parts[:-1]), parts[-1]]) if len(parts) > 1 else parts[0])


def mate_score(item):
    pr = item.get('proof')
    game = 'red' in item
    if not pr or pr['n'] < (2 if game else 3):
        return None
    if not game and pr['n'] < 4 and not pr['sacrifices']:
        return None  # đòn quá ngắn, không thí quân: quá cơ bản cho Shorts
    return (3 * len(pr['sacrifices']) + (2 if len(pr['firsts']) == 1 else 0) + min(pr['n'], 7)
            + (4 if game else 0))


def next_mates(collections, catalog):
    done = {e.get('source_file') for e in catalog['episodes']}
    used = {e['key'] for e in catalog['episodes']}
    pool = []
    for coll in collections:
        data = load_json(ROOT / 'curriculum' / 'mates' / f'{coll}.json', {'items': {}})
        for f, item in data['items'].items():
            sc = mate_score(item)
            if sc is None or f in done or canonical(item['proof']['fen']) in used:
                continue
            pool.append((-sc, coll, f, item))
    # Xoay vòng giữa các nguồn (thực chiến, thí Xe, liên hoàn...), trong mỗi nguồn ưu tiên đòn hay nhất.
    groups = {c: sorted([t for t in pool if t[1] == c], key=lambda t: t[0]) for c in collections}
    out = []
    while any(groups.values()):
        for c in collections:
            if groups[c]:
                _, cc, f, it = groups[c].pop(0)
                out.append((cc, f, it))
    return out


def build_mate(collection, file_name, item, ep, catalog):
    from xq.mate import Prover
    pr = item['proof']
    # Kiểm chứng lại trước khi dựng (chứng minh lặp lại, không tin dữ liệu đã lưu).
    n, firsts = Prover(max_nodes=200_000).solve(pr['fen'], max_n=pr['n'])
    if n != pr['n'] or pr['line'][0]['move'] not in firsts:
        raise ValueError(f'Chứng minh không khớp cho {file_name}')
    side = 'Đỏ' if pr['fen'].split()[1] == 'w' else 'Đen'
    sp = sac_phrase(pr['sacrifices'])
    pos = Position.from_fen(pr['fen'])
    for x in pr['line'][:-1]:
        pos = pos.play(x['move'])
    last = PIECE_VN.get(pos.cells[(ord(pr['line'][-1]['move'][0]) - 97, int(pr['line'][-1]['move'][1]))].upper(), 'Tướng')
    title = f'Sát cục #{ep}: {side} đi, chiếu bí trong {n} nước!'
    game = None
    if 'red' in item:
        from xq.game_episode import year_of
        from xq.players import vn_name
        win = 'w' if pr['fen'].split()[1] == 'w' else 'b'
        winner = vn_name(item['red'] if win == 'w' else item['black'])
        loser = vn_name(item['black'] if win == 'w' else item['red'])
        game = {'winner': winner, 'loser': loser, 'year': year_of(item.get('date')), 'resigned': item.get('resigned'),
                'red': item['red'], 'black': item['black']}
        who = loser or ('Đen' if win == 'w' else 'Đỏ')
        yr = f' ({game["year"]})' if game['year'] else ''
        title = (f'Vì sao {who} xin thua?{yr}' if item.get('resigned') else
                 f'{winner or side} kết thúc ván đấu bằng sát cục {n} nước{yr}')
    yt_title = f'{title}{"" if title[-1] in "!?)" else "!"} Bạn giải được không? #Shorts'
    desc = (f'{side} đi trước, chiếu bí trong {n} nước. Bạn tìm ra không? Đáp án trong video.\n'
            ''
            f'Thế cờ: "{item.get("title", file_name)}" – kho kỳ phổ cộng đồng vietcotuong.com.\n\n'
            '#Shorts #CoTuong #SatCuc #TinhHoaCoTan')
    data = {
        'id': f'ep-{ep:04d}', 'number': ep, 'kind': 'mate', 'topic': f'mate-{collection}',
        'category': 'Sát cục', 'title': title, 'subtitle': 'Sát cục', 'fen': pr['fen'],
        'verdict': {'wdl': 'W', 'dtm': 2 * n - 1}, 'mate': {'n': n, 'line': pr['line'], 'sacrifices': pr['sacrifices'],
                                                          'unique': len(firsts) == 1, 'side': side},
        'source': {'collection': collection, 'file': file_name, 'title': item.get('title')},
        'beats': [], 'analysis': None, 'game': game,
        'youtube_short': {'title': yt_title, 'description': desc,
                          'tags': ['shorts', 'cờ tướng', 'sát cục', 'câu đố cờ tướng', 'tinh hoa cờ tàn']},
    }
    (EPISODES / f'ep-{ep:04d}.json').write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n',
                                               encoding='utf-8')
    catalog['episodes'].append({'ep': ep, 'topic': data['topic'], 'fen': pr['fen'], 'key': canonical(pr['fen']),
                                'title': title, 'source_file': file_name})
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'ep-{ep:04d}: {title}')
    return data


def next_topics(topics, catalog, count, per_pass=2):
    """Thứ tự phát sóng theo vòng: mỗi vòng, mỗi chủ đề thêm tối đa per_pass tập.

    Vòng 1 đi hết giáo trình ở mức cơ bản, các vòng sau quay lại với thế khó hơn,
    tránh phát quá nhiều tập cùng một chủ đề liên tiếp.
    """
    done = {}
    for e in catalog['episodes']:
        done[e['topic']] = done.get(e['topic'], 0) + 1
    out = []
    rounds = max(t.get('episodes', 1) for t in topics) // per_pass + 1
    for r in range(rounds):
        for t in topics:
            target = min(t.get('episodes', 1), (r + 1) * per_pass)
            have = done.get(t['id'], 0)
            if have < target:
                out += [t] * (target - have)
                done[t['id']] = target
    return out[:count]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--count', type=int, default=1)
    ap.add_argument('--topic')
    ap.add_argument('--fen')
    ap.add_argument('--samples', type=int, default=400)
    ap.add_argument('--finalists', type=int, default=6)
    ap.add_argument('--seed', type=int)
    ap.add_argument('--classic', help='tên bộ sưu tập trong curriculum/classics (mặc định theo giáo trình)')
    ap.add_argument('--min-pieces', type=int, default=None,
                    help='bỏ qua thế ít quân hơn mức này; 0 = đi đúng thứ tự sách, kể cả tàn ít quân')
    args = ap.parse_args()
    cur = load_json(CURRICULUM, {})
    topics = cur['topics']
    catalog = load_json(CATALOG, {'episodes': []})
    mate_colls = [] if args.classic or args.topic or args.fen else cur.get('mates', [])
    built = 0
    while mate_colls and built < args.count:
        ep = 1 + max([e['ep'] for e in catalog['episodes']] or [0])
        games = [(c, f, g) for c in cur.get('games', []) for f, g in next_games(c, catalog)]
        if games and ep % cur.get('game_every', 4) == 0:
            build_game(*games[0], ep, catalog)
            built += 1
            continue
        todo = next_mates(mate_colls, catalog)
        if not todo:
            break
        c, f, it = todo[0]
        try:
            build_mate(c, f, it, ep, catalog)
            built += 1
        except ValueError as exc:
            print('CẢNH BÁO:', exc)
            it['proof'] = None
    if mate_colls:
        if built < args.count:
            raise SystemExit(f'Chỉ dựng được {built}/{args.count} tập')
        return
    collections = [args.classic] if args.classic else ([] if args.topic or args.fen else cur.get('classics_first', []))
    game_colls = [] if args.classic or args.topic or args.fen else cur.get('games', [])
    every = cur.get('game_every', 3)
    built = 0
    skip = set()
    while built < args.count and collections:
        ep = 1 + max([e['ep'] for e in catalog['episodes']] or [0])
        games = [(c, f, g) for c in game_colls for f, g in next_games(c, catalog)]
        try:
            if games and ep % every == 0:
                c, f, g = games[0]
                build_game(c, f, g, ep, catalog)
            else:
                min_pieces = cur.get('classics_min_pieces', 0) if args.min_pieces is None else args.min_pieces
                todo = [(c, f, it) for c in collections
                        for f, it in next_classics(c, catalog, min_pieces, include_brief=args.min_pieces == 0)
                        if f not in skip]
                if not todo:
                    break
                c, f, it = todo[0]
                try:
                    build_classic(c, f, it, ep, topics, catalog)
                except (cdb.CdbError, ValueError) as exc:
                    print(f'CẢNH BÁO: bỏ qua {f}: {exc}')
                    skip.add(f)
                    cdb.flush()
                    continue
            built += 1
        finally:
            cdb.flush()
    if built >= args.count or args.classic:
        return
    args.count -= built
    by_id = {t['id']: t for t in topics}
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
