"""Typst -> SVG formula cards, fatal build errors on missing or invalid SVG."""
from pathlib import Path
import shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
FORMULAS={
 'data': '$ (1,2), (2,4), (3,3), (4,5) $',
 'shapes': '$ -1 <= r <= 1 $',
 'pearson': '$ r = frac(36, sqrt(42 times 36)) approx 0.926 $',
 'model': '$ hat(y) = frac(8,7) + frac(6,7) x $',
 'least_squares': '$ SSE = sum (y_i - hat(y)_i)^2 $',
 'prediction': '$ hat(y)(5) = frac(38,7) approx 5.43 $',
 'caution': '$ r = 0 quad "phi tuyến vẫn có thể tồn tại" $',
 'practice': '$ hat(y) = 1 + 2x quad r = 1 $',
}
def create_sources():
    folder=ROOT/'typst/stat17';folder.mkdir(parents=True,exist_ok=True)
    for key,formula in FORMULAS.items():
        (folder/f'{key}.typ').write_text('#set page(width: auto, height: auto, margin: 5pt)\n'
            '#set text(size: 19pt, fill: rgb("#edf6ff"))\n'+formula+'\n',encoding='utf8')

def main():
    create_sources()
    exe=shutil.which('typst')
    if not exe:raise RuntimeError('Typst CLI unavailable: compile in GitHub Actions instead')
    out=ROOT/'assets/stat17_formulas';out.mkdir(parents=True,exist_ok=True)
    for key in FORMULAS:
        source=ROOT/'typst/stat17'/f'{key}.typ';target=out/f'{key}.svg'
        subprocess.run([exe,'compile','--format','svg',str(source),str(target)],check=True)
        if not target.is_file() or target.stat().st_size<150 or '<svg' not in target.read_text(encoding='utf8')[:2000]:
            raise RuntimeError(f'SVG invalid: {target}')
    print('STAT17_TYPST_PASS',len(FORMULAS))
if __name__=='__main__':main()
