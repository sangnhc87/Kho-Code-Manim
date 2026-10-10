#!/usr/bin/env python3
"""Exact verification for episodes 004-006: Knight + high Pawn vs (K + defenders).

Each study is proven by an exhaustive AND-OR mate search (scripts/mate_search.c,
compiled on demand). For every Black reply the search proves Red forces a win in
exactly the stated number of Red moves (checkmate, or Xiangqi stalemate / "bi nuoc",
which is also a loss for the side to move). Repetition and the 60-move rule are
ignored, as in tablebases.

    tap-0004: K+N+P vs K + 1 advisor  + 2 elephants  -> mate in 13 Red moves
    tap-0005: K+N+P vs K + 2 advisors + 1 elephant   -> stalemate in 13 Red moves
    tap-0006: K+N+P vs K + 2 advisors + 2 elephants  -> mate in 13 Red moves
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C_SRC = ROOT / 'scripts' / 'mate_search.c'

STUDIES = {
    'tap-0004': ('3a5/4k4/b3P4/9/2b6/9/1N7/9/9/5K3 w', 13),
    'tap-0005': ('4P1b2/4ak3/5a3/9/7N1/9/9/5K3/9/9 w', 13),
    'tap-0006': ('3a1ab2/3P5/3k4b/9/9/2N6/9/9/9/5K3 w', 13),
}

NODE_CAP = 20000000


def build_binary():
    if not C_SRC.is_file():
        raise SystemExit(f'Missing solver source: {C_SRC}')
    cc = shutil.which('cc') or shutil.which('clang') or shutil.which('gcc')
    if not cc:
        raise SystemExit('No C compiler found (cc/clang/gcc).')
    tmp = Path(tempfile.mkdtemp(prefix='matesearch-'))
    binary = tmp / 'matesearch'
    subprocess.run([cc, '-O2', '-o', str(binary), str(C_SRC)], check=True)
    return binary


def main():
    binary = build_binary()
    ok = True
    for ep, (fen, expected) in STUDIES.items():
        proc = subprocess.run(
            [str(binary), 'dtm', fen, str(expected + 2), str(NODE_CAP)],
            capture_output=True, text=True,
        )
        d = None
        for line in proc.stdout.splitlines():
            if line.startswith('DTM '):
                d = int(line.split()[1])
        status = 'OK' if d == expected else 'FAIL'
        print(f'{ep}: DTM={d} expected={expected} -> {status}')
        ok = ok and d == expected
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
