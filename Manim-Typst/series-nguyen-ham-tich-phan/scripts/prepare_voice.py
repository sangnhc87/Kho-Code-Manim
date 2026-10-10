"""Narration + runtime plan: python scripts/prepare_voice.py --ep int01 --voice on|off"""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import episode, voice  # noqa: E402

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--ep', default='int01')
    ap.add_argument('--voice', choices=['on', 'off'], default='off')
    ap.add_argument('--voice-id', default=voice.VOICE_ID)
    a = ap.parse_args()
    lesson, p = episode.load(a.ep), episode.paths(a.ep)
    plan = asyncio.run(voice.prepare(lesson, p, a.voice, a.voice_id))
    print(f"{plan['episode']}_PREPARE_OK {len(plan['beats'])} beats, "
          f"{plan['total_duration']:.1f}s ({plan['total_duration'] / 60:.1f} min), voice {a.voice}")
