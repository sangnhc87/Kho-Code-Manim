"""Compile a Short's formulas with Typst: python scripts/build_typst.py --short xss001"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import shortlib, typst_build  # noqa: E402

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--short', default='xss001')
    a = ap.parse_args()
    mod, p = shortlib.load(a.short), shortlib.paths(a.short)
    n = typst_build.build(mod.FORMULAS, p['typst_src'], p['formulas'])
    print(f'{mod.EPISODE["code"]}_TYPST_OK {n} formulas')
