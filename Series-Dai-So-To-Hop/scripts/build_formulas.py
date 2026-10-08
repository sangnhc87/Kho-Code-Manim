"""Generate Typst formulas and render them to transparent PNG assets.

Usage: python scripts/build_formulas.py [--write-only]
Compiling requires the `typst` binary (installed by GitHub Actions).
"""
from pathlib import Path
import argparse
import subprocess
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from series_config import PALETTE, symbol

FORMULAS = {
    'sum5': ('2 + 3 = 5', PALETTE['cyan']),
    'sum_general': ('m + n', PALETTE['cyan']),
    'sum7': ('4 + 3 = 7', PALETTE['cyan']),
    'union': ('6 + 4 - 2 = 8', PALETTE['gold']),
    'intersection': ('|A union B| = |A| + |B| - |A inter B|', PALETTE['cyan']),
    'quiz7': ('5 + 2 = 7', PALETTE['green']),
    'arrangement': (symbol('A', 'n', 'k') + ' = frac(n!, (n-k)!)', PALETTE['cyan']),
    'combination': (symbol('C', 'n', 'k') + ' = frac(n!, k! (n-k)!)', PALETTE['cyan']),
    'a63': (symbol('A', '6', '3') + ' = 6 dot 5 dot 4 = 120', PALETTE['cyan']),
    'c53': (symbol('C', '5', '3') + ' = 10', PALETTE['cyan']),
}


def write_typ(name: str, expression: str, color: str) -> Path:
    p = ROOT / 'assets' / 'formulas' / f'{name}.typ'
    text = (
        '#set page(width: 13cm, height: 2.6cm, margin: 0pt, fill: none)\n'
        f'#set text(font: "Noto Serif", size: 27pt, fill: rgb("{color}"))\n'
        f'#align(center + horizon)[$ {expression} $]\n'
    )
    p.write_text(text, encoding='utf-8')
    return p


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--write-only', action='store_true')
    args = ap.parse_args()
    output = ROOT / 'assets' / 'rendered'
    output.mkdir(parents=True, exist_ok=True)
    for name, (expr, color) in FORMULAS.items():
        source = write_typ(name, expr, color)
        if not args.write_only:
            outfile = output / f'{name}.png'
            subprocess.run([
                'typst', 'compile', '--format', 'png', '--ppi', '270',
                str(source), str(outfile)
            ], check=True)
            im = Image.open(outfile).convert('RGBA')
            bbox = im.getchannel('A').getbbox()
            if bbox is None:
                raise RuntimeError(f'Empty Typst formula: {name}')
            margin = 14
            bbox = (max(0,bbox[0]-margin), max(0,bbox[1]-margin),
                    min(im.width,bbox[2]+margin), min(im.height,bbox[3]+margin))
            im.crop(bbox).save(outfile)
    print(f'Prepared {len(FORMULAS)} Typst formulas. compile={not args.write_only}')


if __name__ == '__main__':
    main()
