"""Compile an episode's formulas with Typst: python scripts/build_typst.py --ep int01"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import episode, typst_build  # noqa: E402

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--ep', default='int01')
    a = ap.parse_args()
    lesson, p = episode.load(a.ep), episode.paths(a.ep)
    n = typst_build.build(lesson.FORMULAS, p['typst_src'], p['formulas'])
    print(f'{lesson.EPISODE["code"]}_TYPST_OK {n} formulas')
