"""Generate and (in GitHub) compile eight visible Typst equations to SVG."""
from pathlib import Path
import shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
FORMULAS={
 'overview':'$ Q_1=6 quad Q_2=7 quad Q_3=8 $',
 'ranks':'$ frac(n,4)=10 quad frac(n,2)=20 quad frac(3n,4)=30 $',
 'q1':'$ Q_1 approx 6+frac(10-6,18) times 2 approx 6.44 $',
 'q2':'$ Q_2 approx 6+frac(20-6,18) times 2 approx 7.56 $',
 'q3_iqr':'$ Q_3 approx 8+frac(30-24,14) times 2 approx 8.86 $',
 'ogive':'$ Q_1 approx 6.44 quad Q_2 approx 7.56 quad Q_3 approx 8.86 $',
 'boundaries':'$ Q_1=6 quad Q_2=8 quad Q_3=10 $',
 'reverse':'$ 6+frac(8,x)=6.5 quad x=16 quad "IQR"=2.5 $',
}
def create_sources():
    dest=ROOT/'typst/stat10';dest.mkdir(parents=True,exist_ok=True)
    for name,formula in FORMULAS.items():
        (dest/f'{name}.typ').write_text(
            '#set page(width: auto, height: auto, margin: 5pt)\n'
            '#set text(size: 20pt, fill: rgb("#edf6ff"))\n'
            +formula+'\n',encoding='utf-8')
def main():
    create_sources()
    if not shutil.which('typst'):
        raise RuntimeError('Typst binary is missing: compile this in GitHub Actions')
    dest=ROOT/'assets/stat10_formulas';dest.mkdir(parents=True,exist_ok=True)
    for name in FORMULAS:
        src=ROOT/'typst/stat10'/f'{name}.typ';out=dest/f'{name}.svg'
        subprocess.run(['typst','compile','--format','svg',str(src),str(out)],check=True)
        if not out.is_file() or out.stat().st_size<150:
            raise RuntimeError(f'Invalid SVG compiled for {name}')
        if '<svg' not in out.read_text(encoding='utf-8')[:2000]:
            raise RuntimeError(f'SVG root not found for {name}')
    print('STAT10_TYPST_OK',len(FORMULAS),'SVG images')
if __name__=='__main__':main()
