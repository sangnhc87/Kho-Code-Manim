#!/usr/bin/env python3
"""Nhập 25 hệ khai cục (PGN ký pháp Hán, GBK) thành cây nước đi JSON.

python scripts/import_khaicuc.py  ->  khaicuc/openings/<slug>.json + khaicuc/import_report.json
Mỗi nước trong cây đã được xác nhận hợp lệ bằng luật cờ trong xq/board.py.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from xq import pgn_cn  # noqa: E402
from xq.notation import vn_move  # noqa: E402

SRC = ROOT / 'Khai cục' / 'Khai cuc cap nhat'
OUT = ROOT / 'khaicuc' / 'openings'


def slug(name):
    s = unicodedata.normalize('NFKD', name).replace('đ', 'd').replace('Đ', 'D')
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = []
    for f in sorted(SRC.glob('*.pgn')):
        fen, root = pgn_cn.parse_tree(pgn_cn.decode(f))
        main_line, n = [], root
        while n['children'] and len(main_line) < 8:
            c = n['children'][0]
            main_line.append(vn_move(n['pos'], c['m']))
            n = c
        s = pgn_cn.stats(root)
        data = {'source': f.name, 'slug': slug(f.stem), 'fen': fen, 'stats': s,
                'opening_moves': main_line, 'errors': root['errors'], 'tree': pgn_cn.strip(root)}
        (OUT / f'{data["slug"]}.json').write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
        report.append({k: data[k] for k in ('source', 'slug', 'stats', 'opening_moves')})
        print(f'{f.name:24} {s}')
    (OUT.parent / 'import_report.json').write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding='utf-8')
    bad = sum(r['stats']['errors'] for r in report)
    print(f'Tổng {len(report)} hệ, {sum(r["stats"]["nodes"] for r in report)} nút, {bad} lỗi')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
