"""Compile an episode's FORMULAS dict with the real Typst CLI into SVG files.

Every formula shares one preamble so sizes and colours are identical across
the series. Any Typst error stops the build (no silent fallback).
"""
from __future__ import annotations

import hashlib
import shutil
import subprocess
from pathlib import Path

from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE

FONT_PT = 30
PREAMBLE = f'''#set page(width: auto, height: auto, margin: 2pt, fill: none)
#set text(size: {FONT_PT}pt, fill: rgb("{WHITE}"), font: ("Noto Sans", "Libertinus Serif"))
#let gold(b) = text(fill: rgb("{GOLD}"), b)
#let cyan(b) = text(fill: rgb("{CYAN}"), b)
#let green(b) = text(fill: rgb("{GREEN}"), b)
#let purple(b) = text(fill: rgb("{PURPLE}"), b)
#let coral(b) = text(fill: rgb("{CORAL}"), b)
#let soft(b) = text(fill: rgb("{SOFT}"), b)
'''


def source(expr: str) -> str:
    return PREAMBLE + f'$ {expr} $\n'


def build(formulas: dict[str, str], src_dir: Path, out_dir: Path) -> int:
    if not shutil.which('typst'):
        raise RuntimeError('Typst CLI unavailable; install Typst >= 0.13 (the GitHub Action installs it)')
    src_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    for key, expr in formulas.items():
        typ = src_dir / f'{key}.typ'
        svg = out_dir / f'{key}.svg'
        typ.write_text(source(expr), encoding='utf-8')
        proc = subprocess.run(['typst', 'compile', '--format', 'svg', str(typ), str(svg)],
                              capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f'Typst failed on {key!r}: {expr}\n{proc.stderr}')
        if not svg.exists() or svg.stat().st_size < 300:
            raise RuntimeError(f'Missing formula SVG: {key}')
    return len(formulas)


def inline_key(expr: str, color: str) -> str:
    return 'inl_' + hashlib.sha1(f'{color}|{expr}'.encode('utf-8')).hexdigest()[:12]


def compile_inline(expr: str, color: str, src_dir: Path, out_dir: Path) -> Path:
    """Math segment of a mixed text label (``$...$`` in ``LessonScene.TM``), cached by content."""
    key = inline_key(expr, color)
    svg = out_dir / f'{key}.svg'
    if svg.exists() and svg.stat().st_size >= 300:
        return svg
    if not shutil.which('typst'):
        raise RuntimeError('Typst CLI unavailable; install Typst >= 0.13 (the GitHub Action installs it)')
    src_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    typ = src_dir / f'{key}.typ'
    typ.write_text(PREAMBLE + f'#set text(fill: rgb("{color}"))\n$ {expr} $\n', encoding='utf-8')
    proc = subprocess.run(['typst', 'compile', '--format', 'svg', str(typ), str(svg)], capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f'Typst failed on inline math: {expr}\n{proc.stderr}')
    return svg
