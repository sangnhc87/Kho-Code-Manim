"""Narration + runtime plan: python scripts/prepare_voice.py --short xss001 --voice on|off"""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import shortlib, voice  # noqa: E402

LIMIT = 178.0  # YouTube Shorts: at most 3 minutes

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--short', default='xss001')
    ap.add_argument('--voice', choices=['on', 'off'], default='off')
    a = ap.parse_args()
    mod, p = shortlib.load(a.short), shortlib.paths(a.short)
    plan = asyncio.run(voice.prepare(mod, p, a.voice))
    total = plan['total_duration']
    print(f"{plan['episode']}_PREPARE_OK {len(plan['beats'])} beats, {total:.1f}s, voice {a.voice}")
    if total > LIMIT:
        raise SystemExit(f'{plan["episode"]} is {total:.1f}s: Shorts must stay under {LIMIT:.0f}s')
