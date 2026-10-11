#!/usr/bin/env python3
"""Tìm sát cục kết thúc trong ván thật (curriculum/games/*.json): vì sao bên kia xin thua?

    python scripts/import_game_mates.py Dai-Su-Ky-Lo-Ho-Vinh-Hoa

Với thế cuối ván (hoặc trước nước cuối) mà bên thắng được đi, chứng minh chiếu bí bằng
chuỗi chiếu bất kể đối phương đỡ thế nào. Kết quả ghi curriculum/mates/game-<tên>.json.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from xq.dpxq import replay  # noqa: E402
from xq.mate import Budget, Prover  # noqa: E402

WIN = {'红胜': 'w', '红先胜': 'w', '黑胜': 'b', '红负': 'b'}


def main():
    for name in sys.argv[1:]:
        games = json.loads((ROOT / 'curriculum' / 'games' / f'{name}.json').read_text(encoding='utf-8'))['games']
        out_path = ROOT / 'curriculum' / 'mates' / f'game-{name}.json'
        items = {}
        for f, g in games.items():
            winner = WIN.get(g['result'])
            if not winner:
                continue
            ps = replay(g['start_fen'], g['moves'])
            cands = [i for i in (len(ps) - 1, len(ps) - 2, len(ps) - 3) if i >= 0 and ps[i].turn == winner]
            for i in cands:
                pos = ps[i]
                if pos.is_mate():
                    continue
                pr = Prover(max_nodes=60_000)
                try:
                    n, first = pr.solve(pos.fen(), max_n=7)
                except Budget:
                    continue
                if n and n >= 2:
                    line = pr.main_line(pos.fen(), n, first[0])
                    items[f] = {'title': g['title'], 'red': g['red'], 'black': g['black'], 'date': g['date'],
                                'event': g['event'], 'result': g['result'], 'resigned': not ps[-1].is_mate(),
                                'game_ply': i, 'proof': {'fen': pos.fen(), 'n': n, 'firsts': first, 'line': line,
                                                         'sacrifices': [x['sacrifice'] for x in line if x.get('sacrifice')],
                                                         'start_ply': i, 'pieces': len(pos.cells)}}
                    print(f, 'bí', n, 'nước', items[f]['proof']['sacrifices'], 'xin thua' if items[f]['resigned'] else '', flush=True)
                    break
        out_path.write_text(json.dumps({'source': 'kỳ phổ ván đấu thật (kho cộng đồng vietcotuong.com)',
                                        'collection': f'games/{name}', 'items': items}, ensure_ascii=False, indent=1) + '\n',
                            encoding='utf-8')
        print(name, len(items), 'sát cục kết thúc ván')


if __name__ == '__main__':
    main()
