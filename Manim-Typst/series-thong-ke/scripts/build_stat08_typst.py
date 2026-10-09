"""Build and validate all eight Typst formula SVGs (strict – no silent fallback)."""
from __future__ import annotations
from pathlib import Path
import shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
FORMULAS={
 'midpoints':r'$ m_i = frac(a_i+b_i, 2) quad (m_1,m_2,m_3,m_4)=(5,7,9,11) $',
 'weighted_mean':r'$ bar(x) approx frac(6 times 5+18 times 7+14 times 9+2 times 11, 40)=7.6 $',
 'raw_vs_grouped':r'$ bar(x)_"goc" = 7.1 quad bar(x)_"ghep" approx 7.6 $',
 'new_partition':r'$ bar(x)_"B" approx frac(6 times 5+8 times 6.5+18 times 8+8 times 10,40)=7.65 $',
 'mode_interpolation':r'$ M_o approx 6+frac(18-6,(18-6)+(18-14)) times 2=7.5 $',
 'density_mode':r'$ d_i=frac(n_i,h_i) quad M_o approx 7+frac(9-8,(9-8)+(9-4)) times 2 $',
 'reverse_count':r'$ x=40-6-14-2=18 quad 6+18+14+2=40 $',
 'practice':r'$ bar(x) approx 5.5 quad M_o approx 4+frac(2,2+1) times 2=frac(16,3) $',
}

def create_sources():
    folder=ROOT/'typst/stat08';folder.mkdir(parents=True,exist_ok=True)
    for name,math in FORMULAS.items():
        (folder/f'{name}.typ').write_text(
            '#set page(width: auto, height: auto, margin: 5pt)\n'
            '#set text(size: 20pt, fill: rgb("#edf6ff"))\n'+math+'\n',encoding='utf-8')

def main():
    create_sources()
    if not shutil.which('typst'):
        raise RuntimeError('Typst executable not installed. GitHub Actions will compile these formulas.')
    out=ROOT/'assets/stat08_formulas';out.mkdir(parents=True,exist_ok=True)
    for name in FORMULAS:
        path=out/f'{name}.svg'
        subprocess.run(['typst','compile','--format','svg',str(ROOT/'typst/stat08'/f'{name}.typ'),str(path)],check=True)
        if not path.is_file() or path.stat().st_size<150:
            raise RuntimeError(f'Invalid SVG: {path}')
        if '<svg' not in path.read_text(encoding='utf8')[:1500]:
            raise RuntimeError(f'SVG root is missing: {path}')
    print('STAT08_TYPST_OK',len(FORMULAS),'compiled SVGs')

if __name__=='__main__':main()
