"""Re-flow every PROBLEM into lines of at most LIMIT visible characters (never splitting $…$).
python scripts/wrap_problems.py [--check]
"""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIMIT = 40


def visible(s: str) -> int:
    return len(re.sub(r'[$"]', '', s))


def tokens(text: str) -> list[str]:
    out, buf, inside = [], '', False
    for ch in text:
        if ch == '$':
            inside = not inside
        if ch == ' ' and not inside:
            if buf:
                out.append(buf)
            buf = ''
        else:
            buf += ch
    if buf:
        out.append(buf)
    return out


def wrap(lines: list[str]) -> list[str]:
    if all(visible(l) <= LIMIT for l in lines):
        return lines
    words = tokens(' '.join(lines))
    total = sum(visible(w) + 1 for w in words)
    rows = max(2, -(-total // LIMIT))
    target = total / rows
    out, cur = [], ''
    for w in words:
        cand = (cur + ' ' + w).strip()
        if cur and (visible(cand) > LIMIT or (visible(cur) >= target and len(out) < rows - 1)):
            out.append(cur)
            cur = w
        else:
            cur = cand
    out.append(cur)
    return out


if __name__ == '__main__':
    check = '--check' in sys.argv
    bad = []
    for path in sorted((ROOT / 'xss').glob('xss[0-9][0-9][0-9].py')):
        src = path.read_text('utf-8')
        m = re.search(r'^PROBLEM = (\[.*?\])\n', src, re.S | re.M)
        lines = ast.literal_eval(m.group(1))
        new = wrap(lines)
        if new != lines:
            bad.append(path.stem)
            if not check:
                body = 'PROBLEM = [' + ',\n           '.join(repr(l) for l in new) + ']\n'
                path.write_text(src[:m.start()] + body + src[m.end():], encoding='utf-8')
    print(('TOO_LONG ' if check else 'REWRAPPED ') + ' '.join(bad) if bad else 'PROBLEMS_OK')
    sys.exit(1 if check and bad else 0)
