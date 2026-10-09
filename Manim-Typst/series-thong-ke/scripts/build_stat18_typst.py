"""Typst -> SVG formula cards, fatal build errors on missing or invalid SVG."""
from pathlib import Path
import shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
FORMULAS={
 'population': '$ p = frac(400,1000) = 0.4 = 40% $',
 'random': '$ hat(p) = frac(37,80) = 46.25% $',
 'bias': '$ 70% - 40% = 30 " điểm phần trăm" $',
 'repeats': '$ hat(p) = frac("số chọn A",n) $',
 'standard_error': '$ sigma_(hat(p)) = sqrt(frac(p(1-p),n) dot frac(N-n,N-1)) $',
 'interval': '$ hat(p) plus.minus 1.96 sqrt(frac(hat(p)(1-hat(p)),n)) $',
 'checklist': '$ "Chọn đúng mẫu" arrow "Suy luận phù hợp" $',
 'practice': '$ frac(88,200) = 44% quad frac(150,200) = 75% $',
}

def create_sources():
    folder=ROOT/'typst/stat18';folder.mkdir(parents=True,exist_ok=True)
    for key,formula in FORMULAS.items():
        (folder/f'{key}.typ').write_text('#set page(width: auto, height: auto, margin: 5pt)\n'
            '#set text(size: 19pt, fill: rgb("#edf6ff"))\n'+formula+'\n',encoding='utf8')

def main():
    create_sources()
    exe=shutil.which('typst')
    if not exe:raise RuntimeError('Typst CLI unavailable: compile in GitHub Actions instead')
    out=ROOT/'assets/stat18_formulas';out.mkdir(parents=True,exist_ok=True)
    for key in FORMULAS:
        source=ROOT/'typst/stat18'/f'{key}.typ';target=out/f'{key}.svg'
        subprocess.run([exe,'compile','--format','svg',str(source),str(target)],check=True)
        if not target.is_file() or target.stat().st_size<150 or '<svg' not in target.read_text(encoding='utf8')[:2000]:
            raise RuntimeError(f'SVG invalid: {target}')
    print('STAT18_TYPST_PASS',len(FORMULAS))
if __name__=='__main__':main()
