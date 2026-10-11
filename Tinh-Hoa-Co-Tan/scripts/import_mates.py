#!/usr/bin/env python3
"""Nhập đòn sát cục từ kho kỳ phổ cộng đồng và tự chứng minh bằng tìm kiếm vét cạn.

    python scripts/import_mates.py end-games/连将带杀 end-games/弃车绝杀 ...

Với mỗi thế: đi dọc lời giải của sách, tìm thời điểm sớm nhất mà bên đi có chuỗi chiếu
liên tục dẫn tới bí bất kể đối phương chống đỡ thế nào (chứng minh chính xác).
Lưu curriculum/mates/<bộ sưu tập>.json (chỉ dữ kiện).
"""
import json
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.import_classics import RAW, fetch, list_collection  # noqa: E402
from xq.board import Position  # noqa: E402
from xq.dpxq import parse, replay  # noqa: E402
from xq.mate import Budget, Prover  # noqa: E402

OUT = ROOT / 'curriculum' / 'mates'


def prove(g, max_n=9):
    """Đi ngược từ cuối lời giải: thế sớm nhất (liên tục) còn chứng minh được bí bằng chuỗi chiếu."""
    positions = replay(g['fen'], g['moves'])
    if not positions[-1].is_mate():
        return None
    attacker = positions[-2].turn if len(positions) > 1 else positions[0].turn
    best = None
    last = len(positions) - 1
    for i in range(last - 1, -1, -1):
        pos = positions[i]
        if pos.turn != attacker:
            continue
        remaining = (last - i + 1) // 2
        if remaining > max_n:
            break
        prover = Prover(max_nodes=40_000)
        try:
            n, first = prover.solve(pos.fen(), max_n=remaining)
        except Budget:
            break
        if not n:
            break
        best = (i, pos, n, first, prover)
    if not best:
        return None
    i, pos, n, first, prover = best
    line = prover.main_line(pos.fen(), n, first[0])
    return {'start_ply': i, 'fen': pos.fen(), 'n': n, 'firsts': first, 'line': line,
            'sacrifices': [x['sacrifice'] for x in line if x.get('sacrifice')],
            'pieces': len(pos.cells), 'nodes': prover.nodes}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for coll in sys.argv[1:]:
        name = coll.rstrip('/').split('/')[-1]
        path = OUT / f'{name}.json'
        data = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {
            'source': f'https://github.com/chasoft/community-xiangqi-games-database/tree/main/data/{coll}',
            'collection': coll, 'items': {}}
        files = list_collection(coll)
        print(coll, len(files), 'thế', flush=True)
        for k, f in enumerate(files):
            if f in data['items']:
                continue
            try:
                g = parse(fetch(RAW + urllib.parse.quote(f'{coll}/{f}')))
                proof = prove(g)
            except Exception as exc:
                print('  lỗi', f, str(exc)[:80], flush=True)
                continue
            data['items'][f] = {'title': g['title'], 'start_fen': g['fen'], 'book_moves': g['moves'],
                                'result': g['result'], 'proof': proof}
            if proof:
                print(f'  {f}: bí {proof["n"]} nước, {len(proof["firsts"])} nước đầu đúng, '
                      f'thí {proof["sacrifices"]}, từ nước {proof["start_ply"]}', flush=True)
            if k % 10 == 0:
                path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        ok = [v for v in data['items'].values() if v['proof']]
        print(coll, 'xong:', len(ok), '/', len(data['items']), 'chứng minh được', flush=True)


if __name__ == '__main__':
    main()
