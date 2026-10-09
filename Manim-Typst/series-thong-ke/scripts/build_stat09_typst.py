"""Strictly compile eight STAT09 math formulas to SVG using Typst."""
from pathlib import Path
import shutil, subprocess
ROOT=Path(__file__).resolve().parents[1]
FORMULAS={'raw_vs_grouped': '$ M_e = 7 quad M_e approx 7.56 $', 'cumulative': '$ n=40 quad n/2=20 quad 6 < 20 < 24 $', 'median_class': '$ L=6 quad N_("truoc")=6 quad f=18 quad h=2 $', 'interpolation': '$ M_e approx 6+frac(20-6,18) times 2 approx 7.56 $', 'ogive': '$ frac(M_e-6,2)=frac(20-6,24-6) $', 'regroup': '$ M_e approx 7+frac(20-14,18) times 2 approx 7.67 $', 'boundary': '$ n/2=10 quad M_e approx 4 $', 'practice': '$ M_e approx 4+frac(10-5,7) times 2 approx 5.43 $'}

def create_sources():
    folder=ROOT/'typst/stat09';folder.mkdir(parents=True,exist_ok=True)
    for name,math in FORMULAS.items():
        (folder/f'{name}.typ').write_text(
          '#set page(width: auto, height: auto, margin: 5pt)\n'
          '#set text(size: 20pt, fill: rgb("#edf6ff"))\n'+math+'\n',encoding='utf-8')

def main():
    create_sources()
    if not shutil.which('typst'):
        raise RuntimeError('Typst unavailable; workflow on GitHub will compile SVG.')
    out=ROOT/'assets/stat09_formulas';out.mkdir(parents=True,exist_ok=True)
    for name in FORMULAS:
        source=ROOT/'typst/stat09'/f'{name}.typ'
        path=out/f'{name}.svg'
        subprocess.run(['typst','compile','--format','svg',str(source),str(path)],check=True)
        if not path.is_file() or path.stat().st_size<150:
            raise RuntimeError(f'Invalid SVG: {path}')
        if '<svg' not in path.read_text(encoding='utf-8')[:1500]:
            raise RuntimeError(f'Missing SVG root in: {path}')
    print('STAT09_TYPST_OK',len(FORMULAS),'compiled SVGs')

if __name__=='__main__':main()
