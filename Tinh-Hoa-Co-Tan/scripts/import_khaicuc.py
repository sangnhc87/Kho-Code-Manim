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


MAX_NODES = 6000   # kho "toàn tập" khổng lồ chỉ nhập đến ngân sách này (cắt theo độ sâu), phần còn lại để tra cứu


def prune(tree, max_nodes):
    """Cắt cây theo độ sâu (rộng trước) cho tới khi còn <= max_nodes nút."""
    def count(n):
        return sum(1 + count(c) for c in n.get('c', []))
    if count(tree) <= max_nodes:
        return tree
    for limit in range(60, 0, -1):
        def cut(n, ply_limit=limit):
            kids = [cut(c) for c in n.get('c', []) if c['ply'] <= ply_limit]
            out = {k: v for k, v in n.items() if k != 'c'}
            if kids:
                out['c'] = kids
            return out
        t = cut(tree)
        if count(t) <= max_nodes:
            return t
    return {}


def sources():
    """(đường dẫn, loại): mọi PGN, và XQF nằm ngay trong 'Khai cục' (thư mục con bẫy xử lý riêng)."""
    root = SRC.parent
    out = [(f, 'pgn') for f in sorted(root.rglob('*.pgn'))]
    out += [(f, 'xqf') for f in sorted(root.glob('*.xqf'))]
    return out


def main():
    from xq import xqf
    OUT.mkdir(parents=True, exist_ok=True)
    report, seen = [], set()
    for f, kind in sources():
        try:
            if kind == 'pgn':
                fen, root = pgn_cn.parse_tree(pgn_cn.decode(f))
                tree, errors = pgn_cn.strip(root), root['errors']
                start_pos = root['pos'] if False else None
            else:
                start, xroot, _ = xqf.read(f)
                fen = start.fen()
                tree, errors = xqf.to_tree(xroot, start)
        except Exception as exc:  # file hỏng: ghi nhận, không dừng
            print(f'BỎ QUA {f.name}: {exc!r}')
            continue
        sl = slug(f.stem)
        if sl in seen:
            sl += '-' + kind
        seen.add(sl)
        full = sum(1 for _ in iter_nodes(tree))
        tree = prune(tree, MAX_NODES)
        nodes = sum(1 for _ in iter_nodes(tree))
        data = {'source': str(f.relative_to(SRC.parent)), 'kind': kind, 'slug': sl, 'fen': fen,
                'stats': {'nodes': nodes, 'nodes_in_source': full, 'errors': len(errors)}, 'errors': errors[:5], 'tree': tree}
        (OUT / f'{sl}.json').write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
        report.append({k: data[k] for k in ('source', 'kind', 'slug', 'stats')})
        print(f'{sl:34} {kind} {data["stats"]}')
    (OUT.parent / 'import_report.json').write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'Tổng {len(report)} hệ, {sum(r["stats"]["nodes"] for r in report)} nút')


def iter_nodes(tree):
    stack = list(tree.get('c', []))
    while stack:
        n = stack.pop()
        yield n
        stack.extend(n.get('c', []))


if __name__ == '__main__':
    main()
