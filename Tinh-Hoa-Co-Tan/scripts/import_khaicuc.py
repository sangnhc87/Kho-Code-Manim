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


TERMS = [  # thứ tự quan trọng: cụm dài trước
    ('近代陷阱的发展', 'Bẫy cận đại'), ('古典陷阱的启示', 'Bẫy cổ điển'), ('布局陷阱', 'Bẫy bố cục'),
    ('顺炮', 'Thuận Pháo'), ('列炮局', 'Liệt Pháo'), ('列手炮', 'Liệt Pháo'), ('列炮', 'Liệt Pháo'), ('中炮', 'Pháo đầu'),
    ('屏风马', 'Bình phong mã'), ('三步虎', 'Tam bộ hổ'), ('单提', 'Đơn đề'), ('过宫', 'quá cung'),
    ('巡河车', 'Xe tuần hà'), ('过河车', 'Xe qua hà'), ('直车', 'Xe trực'), ('横车', 'Xe hoành'), ('飞象', 'Phi Tượng'),
    ('夹马炮', 'Pháo kẹp Mã'), ('进卒类', 'tiến Tốt'), ('弃象陷车', 'bỏ Tượng hãm Xe'), ('弃卒陷车', 'bỏ Tốt hãm Xe'),
    ('弃马陷车', 'bỏ Mã hãm Xe'), ('陷车', 'hãm Xe'), ('陷阱', 'bẫy'), ('压马', 'ép Mã'), ('盘河', 'bàn hà'),
    ('对', ' đối '), ('局', ''), ('型', ''), ('马', 'Mã'), ('车', 'Xe'), ('炮', 'Pháo'),
]
FALLBACK_TRAP = 'Bẫy khai cục'


def vi_name(stem, n):
    """Tên tiếng Việt cho file tên Hán; nếu còn chữ Hán chưa dịch được thì dùng tên chung có số thứ tự."""
    import re as _re
    t = _re.sub(r'^[+\-]?\d+', '', stem)
    t = t.replace('（', ' ').replace('）', ' ').replace('(', ' ').replace(')', ' ')
    for zh, vi in TERMS:
        t = t.replace(zh, f' {vi} ')
    t = _re.sub(r'[,，、“”"《》！\s]+', ' ', t).strip()
    if _re.search(r'[\u4e00-\u9fff]', t) or len(t) < 6:
        return f'{FALLBACK_TRAP} số {n}'
    return t[0].upper() + t[1:]


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
    for sub in ('Khai cuc bay chet xe', 'PĐ ma doi'):
        out += [(f, 'trap') for f in sorted((root / sub).glob('*.xqf'))]
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
            else:   # xqf hoặc trap
                start, xroot, _ = xqf.read(f)
                fen = start.fen()
                tree, errors = xqf.to_tree(xroot, start)
        except Exception as exc:  # file hỏng: ghi nhận, không dừng
            print(f'BỎ QUA {f.name}: {exc!r}')
            continue
        n_trap = sum(1 for r in report if r['kind'] == 'trap') + 1
        sl = slug(f.stem) if kind != 'trap' else f'bay-{n_trap:02d}'
        if sl in seen:
            sl += '-' + kind
        seen.add(sl)
        full = sum(1 for _ in iter_nodes(tree))
        tree = prune(tree, MAX_NODES)
        nodes = sum(1 for _ in iter_nodes(tree))
        data = {'source': str(f.relative_to(SRC.parent)), 'kind': kind, 'slug': sl, 'fen': fen,
                'title_vi': vi_name(f.stem, n_trap) if kind == 'trap' else None,
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
