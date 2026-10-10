#!/usr/bin/env python3
"""Exact verification for episodes 004-006: Knight + high Pawn vs (K + defenders).

Uses the memoised AND-OR mate search in scripts/mate_search.py to prove, for each
study, that Red forces a win (checkmate, or Xiangqi stalemate / "bi nuoc" which is
also a loss for the side to move) within a fixed number of Red moves, regardless of
every Black reply. Repetition and the 60-move rule are ignored, as in tablebases.

    tap-0004: K+N+P vs K + 1 advisor  + 2 elephants  -> mate in 6 Red moves
    tap-0005: K+N+P vs K + 2 advisors + 1 elephant   -> stalemate in 6 Red moves
    tap-0006: K+N+P vs K + 2 advisors + 2 elephants  -> mate in 5 Red moves
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT))

from mate_search import MateSolver, from_fen  # noqa: E402

STUDIES = {
    'tap-0004': ('2b2k3/9/4baP2/9/9/N8/9/4K4/9/9 w', 6),
    'tap-0005': ('3a1a3/9/b1P1k4/9/9/3N5/9/5K3/9/9 w', 6),
    'tap-0006': ('3a5/4a4/3kb4/5P3/2b6/9/9/4NK3/9/9 w', 5),
}


def main():
    ok = True
    for ep, (fen, expected) in STUDIES.items():
        b = from_fen(fen)
        S = MateSolver()
        d = S.dtm(b, True, cap=expected + 2)
        status = 'OK' if d == expected else 'FAIL'
        print(f'{ep}: DTM={d} expected={expected} nodes={S.nodes} -> {status}')
        ok = ok and d == expected
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
