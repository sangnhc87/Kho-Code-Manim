"""Render eight math formula cards with Typst to SVG. Fail fast on errors."""
from pathlib import Path
import shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
FORMULAS={
 'question': '$ frac(18,20) = 0.90 quad frac(72,90) = 0.80 $',
 'strata': '$ frac(28,80) = 0.35 quad frac(3,10) = 0.30 $',
 'aggregate': '$ frac(18+28,20+80) = 0.46 quad frac(72+3,90+10) = 0.75 $',
 'weight': '$ 0.2 times 0.90 + 0.8 times 0.35 = 0.46 $',
 'standard': '$ 0.5 times 0.90 + 0.5 times 0.35 = 0.625 $',
 'meaning': '$ frac(46,100) = 0.46 $',
 'pitfalls': '$ frac(18+28,20+80) = 0.46 != 0.625 $',
 'practice': '$ frac(9+8,10+40) = 0.34 quad frac(24+1,30+10) = 0.625 $',
}
def create_sources():
    out=ROOT/'typst/stat16';out.mkdir(parents=True,exist_ok=True)
    for key,formula in FORMULAS.items():
        (out/f'{key}.typ').write_text('#set page(width: auto, height: auto, margin: 5pt)\n'
           '#set text(size: 20pt, fill: rgb("#edf6ff"))\n'+formula+'\n',encoding='utf8')

def main():
    create_sources()
    if not shutil.which('typst'):
        raise RuntimeError('Typst executable unavailable; compile using GitHub Actions')
    out=ROOT/'assets/stat16_formulas';out.mkdir(parents=True,exist_ok=True)
    for key in FORMULAS:
        source=ROOT/'typst/stat16'/f'{key}.typ';target=out/f'{key}.svg'
        subprocess.run(['typst','compile','--format','svg',str(source),str(target)],check=True)
        if not target.is_file() or target.stat().st_size<150 or '<svg' not in target.read_text(encoding='utf8')[:2000]:
            raise RuntimeError(f'Typst SVG invalid: {target}')
    print('STAT16_TYPST_PASS',len(FORMULAS))
if __name__=='__main__':main()
