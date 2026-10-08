"""Compile GEO01 Typst formula cards to transparent PNGs."""
from __future__ import annotations
from pathlib import Path
from subprocess import run
import argparse
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ITEMS = {
    'geo_line': ('y = x - frac(1,2)', '#22D3EE'),
    'geo_bounds': ('frac(13,8) < m < frac(7,4)', '#22C55E'),
    'geo_three': ('x - y + 3 > 0, quad x + 3y - 5 > 0, quad 3 - x - y > 0', '#22D3EE'),
    'geo_final': ('T = 8 dot frac(13,8) + 4 dot frac(7,4) = 20', '#22C55E'),
    'geo_general': ('s D_(AB)(M) > 0, quad s D_(BC)(M) > 0, quad s D_(CA)(M) > 0', '#22D3EE'),
    'geo_boundary': ('s D_(AB)(M) >= 0, quad s D_(BC)(M) >= 0, quad s D_(CA)(M) >= 0', '#FBBF24'),
    'geo_bary': ('alpha > 0, quad beta > 0, quad gamma > 0', '#22D3EE'),
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-only',action='store_true')
    args=parser.parse_args()
    src = ROOT / 'assets' / 'formulas'
    dst = ROOT / 'assets' / 'rendered'
    src.mkdir(parents=True,exist_ok=True)
    dst.mkdir(parents=True,exist_ok=True)
    for name,(expr,color) in ITEMS.items():
        text=(
            '#set page(width: 17cm, height: 3cm, margin: 0pt, fill: none)\n'
            f'#set text(font: "Noto Serif", size: 29pt, fill: rgb("{color}"))\n'
            f'#align(center + horizon)[$ {expr} $]\n'
        )
        infile=src/f'{name}.typ'
        infile.write_text(text,encoding='utf-8')
        if not args.write_only:
            outfile=dst/f'{name}.png'
            run(['typst','compile','--format','png','--ppi','250',str(infile),str(outfile)],check=True)
            im=Image.open(outfile).convert('RGBA')
            alpha=im.getchannel('A')
            bbox=alpha.getbbox()
            if bbox is None:
                raise RuntimeError(f'Empty Typst asset: {name}')
            pad=16
            rect=(max(0,bbox[0]-pad),max(0,bbox[1]-pad),
                  min(im.width,bbox[2]+pad),min(im.height,bbox[3]+pad))
            im.crop(rect).save(outfile)
        print(f'{name}: {expr}')
    print(f'Prepared {len(ITEMS)} formulas, compiled={not args.write_only}')

if __name__=='__main__':
    main()
