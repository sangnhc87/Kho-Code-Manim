"""Compile Typst maths to vector SVG for Manim (no LaTeX installation)."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1]
FORMULAS={
 'freq_sum': r'$ sum_(i=1)^7 f_i = 40 $',
 'relative': r'$ p_i = f_i / 40 times 100% $',
 'score_ge_8': r'$ 8 + 6 + 2 = 16 $',
 'checks': r'$ sum_(i=1)^7 p_i = 100% $',
}
def main():
    out=ROOT/'assets'/'formulas'
    out.mkdir(parents=True,exist_ok=True)
    for name,formula in FORMULAS.items():
        typ=ROOT/'typst'/f'{name}.typ'
        typ.write_text('#set page(width: auto, height: auto, margin: 5pt)\n'
                       '#set text(fill: rgb("#eef7ff"), size: 24pt)\n'
                       f'{formula}\n',encoding='utf8')
        subprocess.run(['typst','compile','--format','svg',str(typ),str(out/f'{name}.svg')],check=True)
        assert (out/f'{name}.svg').stat().st_size>100
        print('Typst SVG:',name)
if __name__=='__main__':main()
