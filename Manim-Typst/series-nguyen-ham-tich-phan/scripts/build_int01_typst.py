"""Compile math from one authoritative source, fail if Typst is missing or invalid."""
from __future__ import annotations
import sys,subprocess,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from int01.lesson import FORMULAS

def build():
    if not shutil.which('typst'):
        raise RuntimeError('Typst CLI unavailable; install Typst >=0.13 (GitHub Action installs it)')
    source=ROOT/'typst/int01'; source.mkdir(parents=True,exist_ok=True)
    target=ROOT/'assets/int01_formulas'; target.mkdir(parents=True,exist_ok=True)
    for key,expr in FORMULAS.items():
        content=('''#set page(width: auto, height: auto, margin: 2pt, fill: none)\n#set text(size: 29pt, fill: rgb("#F1F5F9"))\n$'''+expr+'$\n')
        file=source/f'{key}.typ'
        file.write_text(content,encoding='utf-8')
        svg=target/f'{key}.svg'
        subprocess.run(['typst','compile','--format','svg',str(file),str(svg)],check=True)
        if not svg.exists() or svg.stat().st_size<300:raise RuntimeError(f'Missing formula SVG: {key}')
    print('INT01_TYPST_OK',len(FORMULAS))
if __name__=='__main__':build()
