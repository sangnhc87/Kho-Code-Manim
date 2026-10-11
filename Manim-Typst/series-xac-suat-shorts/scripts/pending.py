"""Shorts that are produced (xss/xssNNN.py exists) but not yet on YouTube, in order.
python scripts/pending.py [--limit N] [--select 1-10|xss003,xss007|pending]  → JSON list for a CI matrix
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import shortlib  # noqa: E402

HISTORY = ROOT.parents[1] / 'youtube_uploaded_history.json'


def uploaded() -> set[str]:
    try:
        return {k for k in json.loads(HISTORY.read_text('utf-8')) if k.startswith('xss_')}
    except FileNotFoundError:
        return set()


def select(spec: str) -> list[str]:
    done = uploaded()
    made = shortlib.produced()
    if spec in ('', 'pending'):  # only reviewed Shorts (ready.json) are published automatically
        ready = json.loads((ROOT / 'ready.json').read_text('utf-8'))['ready']
        ok = lambda n: any(a <= n <= b for a, b in ready)  # noqa: E731
        return [c for c in made if f'xss_{c[3:]}' not in done and ok(int(c[3:]))]
    out = []
    for part in spec.split(','):
        m = re.fullmatch(r'(?:xss)?0*(\d+)\s*-\s*(?:xss)?0*(\d+)', part.strip())
        if m:
            out += [f'xss{i:03d}' for i in range(int(m.group(1)), int(m.group(2)) + 1)]
        elif part.strip():
            out.append(shortlib.normalise(part))
    return [c for c in out if c in made]


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--select', default='pending')
    ap.add_argument('--limit', type=int, default=0)
    a = ap.parse_args()
    items = select(a.select)
    if a.limit:
        items = items[:a.limit]
    print(json.dumps(items))
