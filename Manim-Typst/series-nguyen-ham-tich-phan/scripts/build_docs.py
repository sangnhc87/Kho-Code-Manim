"""Teacher script (lời giảng) for an episode, generated from intXX/lesson.py.

python scripts/build_docs.py --ep int01   ->   LOI_GIANG_INT01.md
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import episode  # noqa: E402

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--ep', default='int01')
    a = ap.parse_args()
    lesson = episode.load(a.ep)
    ep = lesson.EPISODE
    parts = dict(lesson.PARTS)
    out = [f"# {ep['code']} – {ep['title']}: {ep['subtitle']}", '',
           f'> Sinh tự động từ `{a.ep}/lesson.py` – sửa lời giảng ở đó rồi chạy lại '
           f'`python scripts/build_docs.py --ep {a.ep}`.', '',
           f'**Số nhịp:** {len(lesson.BEATS)} · **Số công thức Typst:** {len(lesson.FORMULAS)} · '
           f'**Từ:** {sum(len(b.text.split()) for b in lesson.BEATS)}', '']
    current = None
    for b in lesson.BEATS:
        if b.part != current:
            current = b.part
            out += [f'## {parts[b.part]}', '']
        if b.chapter:
            out += [f'### ⏱ {b.chapter}', '']
        out += [f'**`{b.id}`** — {b.text}', '']
    out += ['## Bài tập tự luyện', '']
    out += [f'{i}. {q} → **{ans}**' for i, (q, ans) in enumerate(lesson.EXERCISES, 1)]
    target = ROOT / f"LOI_GIANG_{ep['code']}.md"
    target.write_text('\n'.join(out) + '\n', encoding='utf-8')
    print('wrote', target.name)
