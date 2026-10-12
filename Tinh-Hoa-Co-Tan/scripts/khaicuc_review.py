#!/usr/bin/env python3
"""Tạo khaicuc/REVIEW.md: bảng để người duyệt đối chiếu tên hệ khai cục với nước đi thật (tên ở khaicuc/meta.json)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from xq.board import Position  # noqa: E402
from xq.notation import vn_move  # noqa: E402

meta = json.loads((ROOT / 'khaicuc' / 'meta.json').read_text(encoding='utf-8'))
rows = ['# Duyệt tên các hệ khai cục', '',
        'Sửa cột `name` / `tagline` trong `khaicuc/meta.json` rồi đặt `"reviewed": true`. '
        'Cột "Nước đầu" lấy từ biến chính của file nguồn để đối chiếu.', '',
        '| # | slug | Tên hiện tại | Mô tả ngắn | Nước đầu (biến chính) | Số nút | Đã duyệt |', '|---|---|---|---|---|---|---|']
n = 0
for e in meta['syllabus']:
    if e['slug'] == '@traps':
        continue
    n += 1
    d = json.loads((ROOT / 'khaicuc' / 'openings' / f'{e["slug"]}.json').read_text(encoding='utf-8'))
    pos, node, seq = Position.from_fen(d['fen']), d['tree'], []
    while node.get('c') and len(seq) < 8:
        c = node['c'][0]
        seq.append(f'{(c["ply"] + 1) // 2}{"." if c["ply"] % 2 else "…"}{vn_move(pos, c["m"])}')
        pos, node = pos.play(c['m']), c
    rows.append(f'| {n} | {e["slug"]} | {e["name"]} | {e["tagline"]} | {" ".join(seq)} | {d["stats"]["nodes"]} | {"✅" if e["reviewed"] else "⬜"} |')
rows += ['', '## Thế bẫy (40 file XQF)', '',
         'Tên Việt chỉ đặt khi dịch được chắc chắn từ tên file Hán; còn lại là "Bẫy khai cục số N".', '',
         '| slug | Tên | Số nút |', '|---|---|---|']
for f in sorted((ROOT / 'khaicuc' / 'openings').glob('bay-*.json')):
    d = json.loads(f.read_text(encoding='utf-8'))
    rows.append(f'| {d["slug"]} | {d["title_vi"]} | {d["stats"]["nodes"]} |')
(ROOT / 'khaicuc' / 'REVIEW.md').write_text('\n'.join(rows) + '\n', encoding='utf-8')
print('Đã ghi khaicuc/REVIEW.md', n, 'hệ')
