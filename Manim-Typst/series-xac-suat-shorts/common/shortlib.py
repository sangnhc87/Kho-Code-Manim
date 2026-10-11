"""Locate and load one Short (xss001 … xss120) and its paths."""
from __future__ import annotations

import importlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def normalise(code: str) -> str:
    m = re.fullmatch(r'(?i)(?:xss)?0*(\d{1,3})', str(code).strip())
    if not m or not 1 <= int(m.group(1)) <= 999:
        raise SystemExit(f'Invalid short {code!r}: expected xss001 …')
    return f'xss{int(m.group(1)):03d}'


def plan_entry(n: int) -> dict:
    plan = json.loads((ROOT / 'shorts_plan.json').read_text('utf-8'))
    return plan['shorts'][n - 1]


def load(code: str):
    """Return the ``xss.xssNNN`` module after checking it against the verified plan."""
    name = normalise(code)
    mod = importlib.import_module(f'xss.{name}')
    n = int(name[3:])
    entry = plan_entry(n)
    assert mod.EPISODE['code'] == name.upper(), name
    assert mod.EPISODE['answer'] == entry['answer'], (mod.EPISODE['answer'], entry['answer'])
    ids = [b.id for b in mod.BEATS]
    assert ids[0] == 'hook' and ids[-1] == 'outro' and len(ids) == len(set(ids)), ids
    if hasattr(mod, 'validate'):
        assert mod.validate() is True
    return mod


def produced() -> list[str]:
    return sorted(p.stem for p in (ROOT / 'xss').glob('xss[0-9][0-9][0-9].py'))


def paths(code: str) -> dict[str, Path]:
    name = normalise(code)
    return {
        'name': Path(name),
        'pkg': ROOT / 'xss',
        'formulas': ROOT / 'assets' / name,
        'typst_src': ROOT / 'typst' / name,
        'voice': ROOT / 'voice' / name,
        'plan': ROOT / 'plans' / f'{name}.json',
        'timeline': ROOT / 'artifacts' / f'{name}_timeline.json',
        'srt': ROOT / 'artifacts' / f'{name.upper()}_vi.srt',
        'artifacts': ROOT / 'artifacts' / f'{name}_qa',
        'youtube': ROOT / 'artifacts' / f'{name}_youtube.json',
    }
