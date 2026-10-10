"""Locate and load an episode package (int01, int02, ...)."""
from __future__ import annotations

import importlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def normalise(ep: str) -> str:
    m = re.fullmatch(r'(?i)(?:int)?0*(\d{1,2})', ep.strip())
    if not m or not 1 <= int(m.group(1)) <= 36:
        raise SystemExit(f'Invalid episode {ep!r}: expected int01 … int36')
    return f'int{int(m.group(1)):02d}'


def load(ep: str):
    """Return the validated ``intXX.lesson`` module."""
    name = normalise(ep)
    lesson = importlib.import_module(f'{name}.lesson')
    lesson.validate()
    return lesson


def paths(ep: str) -> dict[str, Path]:
    name = normalise(ep)
    code = name.upper()
    return {
        'name': Path(name),
        'pkg': ROOT / name,
        'formulas': ROOT / 'assets' / f'{name}_formulas',
        'typst_src': ROOT / 'typst' / name,
        'voice': ROOT / name / 'voice',
        'plan': ROOT / name / 'runtime_plan.json',
        'timeline': ROOT / 'artifacts' / f'{name}_timeline.json',
        'srt': ROOT / f'{code}_vi.srt',
        'artifacts': ROOT / 'artifacts' / f'{name}_qa',
        'youtube': ROOT / 'artifacts' / f'{name}_youtube_description.txt',
    }
