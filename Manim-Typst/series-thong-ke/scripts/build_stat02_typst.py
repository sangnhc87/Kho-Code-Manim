"""Compile only STAT02's vector formulas to SVG using Typst."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1]
FORMULAS={
 'bar':r'$ f_7 = 10 $',
 'pie':r'$ 10/40 times 360 = 90 $',
 'percentage':r'$ 16/40 times 100% = 40% $',
 'density':r'$ h_i = f_i / (b_i - a_i) $',
 'line':r'$ Delta = 7.2 - 6.4 = 0.8 $',
 'reading':r'$ N = sum_i f_i $',
}
def main():
    root=ROOT/'typst'/'stat02'
    target=ROOT/'assets'/'stat02_formulas'
    root.mkdir(parents=True,exist_ok=True)
    target.mkdir(parents=True,exist_ok=True)
    for key,formula in FORMULAS.items():
        src=root/f'{key}.typ'
        src.write_text('#set page(width: auto, height: auto, margin: 6pt)\n'
                       '#set text(fill: rgb("#eef7ff"), size: 25pt)\n'
                       +formula+'\n',encoding='utf-8')
        output=target/f'{key}.svg'
        subprocess.run(['typst','compile','--format','svg',str(src),str(output)],check=True)
        assert output.is_file() and output.stat().st_size>100
        print('Typst vector asset:',output.relative_to(ROOT))
if __name__=='__main__':main()
