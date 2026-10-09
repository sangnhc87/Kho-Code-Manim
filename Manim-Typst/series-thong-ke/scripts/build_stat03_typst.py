"""Build STAT03 Typst math, and fail if a formula does not compile."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1]
FORMULAS={
 'overview':r'$ (284) / 40 = 7.1 $',
 'mean':r'$ bar(x) = (sum_i f_i x_i) / (sum_i f_i) = 7.1 $',
 'median':r'$ Me = (x_20 + x_21) / 2 = 7 $',
 'mode':r'$ Mo = 7 quad (f_7 = 10) $',
 'outlier':r'$ (63 - 9 + 27) / 9 = 9 $',
 'compare':r'$ bar(x) = 7.1 quad Me = 7 quad Mo = 7 $',
 'shift':r'$ bar(y) = bar(x) + 2 = 9.1 $',
 'exercise':r'$ 5 times 7 - (5 + 6 + 7 + 8) = 9 $',
}
def main():
    dest=ROOT/'assets'/'stat03_formulas'; dest.mkdir(parents=True,exist_ok=True)
    outdir=ROOT/'typst'/'stat03'; outdir.mkdir(parents=True,exist_ok=True)
    for key,expr in FORMULAS.items():
        src=outdir/f'{key}.typ'
        src.write_text('#set page(width: auto, height: auto, margin: 5pt)\n'
                       '#set text(size: 23pt, fill: rgb("#ecf7ff"))\n'
                       +expr+'\n',encoding='utf-8')
        dest_file=dest/f'{key}.svg'
        subprocess.run(['typst','compile','--format','svg',str(src),str(dest_file)],check=True)
        if not dest_file.is_file() or dest_file.stat().st_size<100:raise RuntimeError(f'Empty Typst formula {key}')
    print('STAT03 Typst formula SVGs compiled:',len(FORMULAS))
if __name__=='__main__':main()
