"""Compile eight real Typst formulas to SVG. Fail immediately if any SVG is absent or invalid."""
from pathlib import Path
import shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
FORMULAS={
 'intervals':r'$ n_1 + n_2 + n_3 + n_4 = 6 + 18 + 14 + 2 = 40 $',
 'boundary':r'$ 4 <= x < 6 quad 6 <= x < 8 $',
 'cumulative':r'$ N_1 = 6 quad N_2 = 24 quad N_3 = 38 quad N_4 = 40 $',
 'relative':r'$ f_i = frac(n_i, 40) quad sum_(i=1)^4 f_i = 1 $',
 'density':r'$ h_i = frac(n_i, b_i - a_i) quad A_i = h_i (b_i - a_i) = n_i $',
 'approximation':r'$ bar(x) approx frac(5 times 6 + 7 times 18 + 9 times 14 + 11 times 2, 40) = 7.6 $',
 'grouping':r'$ 3 times 2 + 8 times 1 + 9 times 2 + 4 times 2 = 40 $',
 'practice':r'$ 5 + 7 + 6 + 2 = 20 $',
}
def create_sources():
    folder=ROOT/'typst'/'stat07';folder.mkdir(parents=True,exist_ok=True)
    for name,expression in FORMULAS.items():
        (folder/f'{name}.typ').write_text(
          '#set page(width: auto, height: auto, margin: 5pt)\n'
          '#set text(size: 20pt, fill: rgb("#edf6ff"))\n'+expression+'\n',encoding='utf8')
def main():
    create_sources()
    if not shutil.which('typst'):raise RuntimeError('Typst CLI missing: install and retry')
    folder=ROOT/'assets'/'stat07_formulas';folder.mkdir(parents=True,exist_ok=True)
    for name in FORMULAS:
        dest=folder/f'{name}.svg'
        subprocess.run(['typst','compile','--format','svg',str(ROOT/'typst/stat07'/f'{name}.typ'),str(dest)],check=True)
        if not dest.is_file() or dest.stat().st_size<150:raise RuntimeError(f'Empty SVG: {dest}')
        if '<svg' not in dest.read_text(encoding='utf8')[:1200]:raise RuntimeError(f'Invalid SVG: {dest}')
    print('STAT07_TYPST_OK',len(FORMULAS))
if __name__=='__main__':main()
