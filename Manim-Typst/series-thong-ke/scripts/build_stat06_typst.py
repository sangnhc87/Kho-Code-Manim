"""Make and compile all Typst formulas to SVG; nonzero exit on any failure."""
from pathlib import Path
import subprocess,shutil
ROOT=Path(__file__).resolve().parents[1]
FORMULAS={
 'compare':r'$ bar(x)_A = bar(x)_B = 7 quad s_A^2 = 2 quad s_B^2 = 18 $',
 'square':r'$ (-2)^2 + (-1)^2 + 0^2 + 1^2 + 2^2 = 10 $',
 'definition':r'$ s^2 = frac(1, n) sum_(i=1)^n (x_i - bar(x))^2 $',
 'frequency':r'$ s^2 = frac(2108, 40) - 7.1^2 = 2.29 $',
 'spread':r'$ s_A = sqrt(2) quad s_B = sqrt(18) $',
 'transform':r'$ "Var"(a x + b) = a^2 "Var"(x) $',
 'outlier':r'$ s^2 = 72.7 - 7.6^2 = 14.94 $',
 'exercise':r'$ s^2 = 8 quad s = 2 sqrt(2) $',
}

def create_sources():
    folder=ROOT/'typst'/'stat06';folder.mkdir(parents=True,exist_ok=True)
    for name,expression in FORMULAS.items():
        (folder/f'{name}.typ').write_text(
          '#set page(width: auto, height: auto, margin: 5pt)\n'
          '#set text(size: 20pt, fill: rgb("#edf6ff"))\n'
          +expression+'\n',encoding='utf-8')

def main():
    create_sources()
    if not shutil.which('typst'):raise RuntimeError('Typst CLI missing: install and retry')
    folder=ROOT/'assets'/'stat06_formulas';folder.mkdir(parents=True,exist_ok=True)
    for name in FORMULAS:
        dest=folder/f'{name}.svg'
        subprocess.run(['typst','compile','--format','svg',str(ROOT/'typst/stat06'/f'{name}.typ'),str(dest)],check=True)
        if not dest.is_file() or dest.stat().st_size<150:
            raise RuntimeError('No SVG generated: '+str(dest))
        if '<svg' not in dest.read_text(encoding='utf-8')[:1200]:
            raise RuntimeError('Invalid SVG: '+str(dest))
    print('STAT06_TYPST_OK',len(FORMULAS))

if __name__=='__main__':main()
