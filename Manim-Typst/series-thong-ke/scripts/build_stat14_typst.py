"""Build eight formula SVGs with Typst; any failed compile stops the workflow."""
from __future__ import annotations
from pathlib import Path
import shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
FORMULAS={
    'context': '$ overline(x)_A=overline(x)_B=8 quad M_A=M_B=8 $',
    'dispersion': '$ s_A^2=1.2 quad s_B^2=15 $',
    'criteria': '$ 10/10=1 quad 8/10=0.8 $',
    'outlier': '$ overline(x)_"truoc"=8 quad overline(x)_"sau"=10 $',
    'grouped': '$ overline(x)_"goc"=7.1 quad overline(x)_"nhom" approx 7.6 $',
    'weighted': '$ overline(x)=(10 times 8+30 times 6)/40=6.5 $',
    'responsible': '$ overline(x) quad M quad s quad "IQR" $',
    'exercise': '$ s_C^2=2 < 11.5=s_D^2 quad "IQR"_C=1.5 < 4="IQR"_D $',
}

def create_sources():
    dest=ROOT/'typst/stat14';dest.mkdir(parents=True,exist_ok=True)
    for key,value in FORMULAS.items():
        (dest/f'{key}.typ').write_text(
            '#set page(width: auto, height: auto, margin: 5pt)\n'
            '#set text(size: 20pt, fill: rgb("#edf6ff"))\n'+value+'\n',encoding='utf-8')

def main():
    create_sources()
    if not shutil.which('typst'):
        raise RuntimeError('Typst is missing: run compilation in GitHub Actions')
    dest=ROOT/'assets/stat14_formulas';dest.mkdir(parents=True,exist_ok=True)
    for key in FORMULAS:
        src=ROOT/'typst/stat14'/f'{key}.typ';target=dest/f'{key}.svg'
        subprocess.run(['typst','compile','--format','svg',str(src),str(target)],check=True)
        if not target.exists() or target.stat().st_size<150:
            raise RuntimeError(f'Typst output is missing or empty: {key}')
        if '<svg' not in target.read_text(encoding='utf-8')[:2000]:
            raise RuntimeError(f'Not SVG: {key}')
    print('STAT14_TYPST_PASS',len(FORMULAS))

if __name__=='__main__':main()
