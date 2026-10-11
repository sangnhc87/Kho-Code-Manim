#!/usr/bin/env python3
"""Chấm tàn cuộc trong ván đấu thật bằng bảng tra chessdb.

    python scripts/import_games.py selected-games/Dai-Su-Ky-Lo-Ho-Vinh-Hoa [--limit 80]

Với mỗi ván: chạy lại kỳ phổ, tìm thế sớm nhất (tính từ cuối ván ngược lên) còn nằm trong
bảng tra, rồi chấm từng nước thật: giữ kết quả hay làm hỏng (thắng→hòa, hòa→thua...),
có phải nước duy nhất không. Lưu vào curriculum/games/<bộ sưu tập>.json (chỉ dữ kiện).
"""
import argparse
import json
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.import_classics import RAW, fetch, list_collection  # noqa: E402
from xq import cdb  # noqa: E402
from xq.dpxq import parse, replay  # noqa: E402

OUT = ROOT / 'curriculum' / 'games'
MAX_PIECES = 14
RANK = {'W': 2, 'D': 1, 'L': 0}


def value(pos):
    res = cdb.query(pos.fen())
    if res['status'] == 'mate':
        return {'wdl': 'L', 'dtm': 0, 'moves': []}
    if res['status'] != 'egtb':
        return None
    return {'wdl': res['moves'][0]['wdl'], 'dtm': res['moves'][0]['dtm'], 'moves': res['moves']}


def score_game(g):
    positions = replay(g['fen'], g['moves'])
    moves = g['moves'][:len(positions) - 1]
    # Tìm thế sớm nhất trong bảng tra (đi ngược từ cuối ván).
    entry = None
    vals = {}
    for i in range(len(positions) - 1, -1, -1):
        pos = positions[i]
        if sum(1 for _ in pos.cells) > MAX_PIECES:
            break
        try:
            v = value(pos)
        except (cdb.CdbError, ValueError):
            v = None
        if v is None:
            break
        vals[i] = v
        entry = i
    if entry is None or entry >= len(moves):
        return None
    plies = []
    for i in range(entry, len(moves)):
        v = vals[i]
        m = moves[i]
        played = next((x for x in v['moves'] if x['move'] == m), None)
        if played is None:
            break
        keep = [x for x in v['moves'] if x['wdl'] == v['wdl']]
        plies.append({'i': i, 'fen': positions[i].fen(), 'move': m, 'side': positions[i].turn,
                      'before': v['wdl'], 'after': played['wdl'], 'dtm_best': v['dtm'], 'dtm_played': played['dtm'],
                      'n_keep': len(keep), 'n_legal': len(v['moves']), 'best': v['moves'][0]['move'],
                      'error': RANK[played['wdl']] < RANK[v['wdl']],
                      'only_found': len(keep) == 1 and len(v['moves']) > 1 and played['wdl'] == v['wdl']})
    if not plies:
        return None
    return {'entry_ply': entry, 'entry_fen': positions[entry].fen(), 'entry_value': vals[entry]['wdl'],
            'entry_dtm': vals[entry]['dtm'], 'pieces': len(positions[entry].cells), 'plies': plies,
            'errors': sum(p['error'] for p in plies), 'only_found': sum(p['only_found'] for p in plies)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('collections', nargs='+')
    ap.add_argument('--limit', type=int, default=10 ** 6)
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    for coll in args.collections:
        name = coll.rstrip('/').split('/')[-1]
        path = OUT / f'{name}.json'
        data = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {
            'source': f'https://github.com/chasoft/community-xiangqi-games-database/tree/main/data/{coll}',
            'collection': coll, 'games': {}}
        files = list_collection(coll)[:args.limit]
        print(coll, len(files), 'ván', flush=True)
        for k, f in enumerate(files):
            if f in data['games']:
                continue
            try:
                g = parse(fetch(RAW + urllib.parse.quote(f'{coll}/{f}')))
                s = score_game(g)
            except Exception as exc:
                print('  lỗi', f, str(exc)[:100])
                continue
            data['games'][f] = {'red': g['red'], 'black': g['black'], 'event': g['event'], 'date': g['date'],
                                'result': g['result'], 'title': g['title'], 'n_moves': len(g['moves']),
                                'start_fen': g['fen'], 'moves': g['moves'], 'endgame': s}
            if s:
                print(f'  {k} {f}: vào bảng tra ở nước {s["entry_ply"]} ({s["pieces"]} quân, {s["entry_value"]}), '
                      f'{len(s["plies"])} nước chấm, {s["errors"]} sai lầm, {s["only_found"]} nước duy nhất', flush=True)
            if k % 5 == 0:
                cdb.flush()
                path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        cdb.flush()
        path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
