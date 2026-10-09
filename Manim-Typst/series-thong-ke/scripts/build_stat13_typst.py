"""Build eight formula SVGs with Typst; any failed compile stops the workflow."""
from __future__ import annotations
from pathlib import Path
import shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
FORMULAS={
    'problem': '$ overline(x)_A=overline(x)_B=7 $',
    'central': '$ overline(x)_A=overline(x)_B=7 quad M_A=M_B=7 $',
    'boxplot': '$ "IQR"_A=8-6=2 quad "IQR"_B=10-4=6 $',
    'dispersion': '$ s_A^2=12/10=1.2 quad s_B^2=54/10=5.4 $',
    'grouped': '$ overline(x)_A approx overline(x)_B approx 7.6 $',
    'targets': '$ 9/10=0.9 quad 7/10=0.7 $',
    'limits': '$ s_A < s_B quad "trong mẫu đã cho" $',
    'exercise': '$ "IQR"_A=2 quad "IQR"_B=5 quad s_A^2=1.5 < 5.5=s_B^2 $',
}

def create_sources():
    dest=ROOT/'typst/stat13';dest.mkdir(parents=True,exist_ok=True)
    for key,value in FORMULAS.items():
        (dest/f'{key}.typ').write_text(
            '#set page(width: auto, height: auto, margin: 5pt)\n'
            '#set text(size: 20pt, fill: rgb("#edf6ff"))\n'+value+'\n',encoding='utf-8')

def main():
    create_sources()
    if not shutil.which('typst'):
        raise RuntimeError('Typst is missing: run compilation in GitHub Actions')
    dest=ROOT/'assets/stat13_formulas';dest.mkdir(parents=True,exist_ok=True)
    for key in FORMULAS:
        src=ROOT/'typst/stat13'/f'{key}.typ';target=dest/f'{key}.svg'
        subprocess.run(['typst','compile','--format','svg',str(src),str(target)],check=True)
        if not target.exists() or target.stat().st_size<150:
            raise RuntimeError(f'Typst output is missing or empty: {key}')
        if '<svg' not in target.read_text(encoding='utf-8')[:2000]:
            raise RuntimeError(f'Not SVG: {key}')
    print('STAT13_TYPST_PASS',len(FORMULAS))

if __name__=='__main__':main()
