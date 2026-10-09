"""Generate and compile 8 SVGs; fail hard on missing Typst or invalid output."""
from pathlib import Path
import shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
FORMULAS={
'intro':'$ n=40 quad m=(5,7,9,11) $',
'centers':'$ overline(x) approx (6 times 5+18 times 7+14 times 9+2 times 11)/40=7.6 $',
'variance':'$ s^2 approx 97.6/40=2.44 quad s approx sqrt(2.44) $',
'shortcut':'$ s^2 approx 2408/40 - 7.6^2 = 2.44 $',
'compare':'$ overline(x)_A=overline(x)_B=7.6 quad s_A^2=2.44 < s_B^2=4.44 $',
'transforms':'$ s^2(a x+b)=a^2 s^2(x) quad s(a x+b)=abs(a) s(x) $',
'outlier':'$ s^2_"gốc"=2.29 quad s^2_"mới"=14.94 $',
'practice':'$ x=2 quad s^2 approx 3.36 quad s approx 1.833 $',
}
def create_sources():
    dest=ROOT/'typst/stat12';dest.mkdir(parents=True,exist_ok=True)
    for key,value in FORMULAS.items():
        (dest/f'{key}.typ').write_text('#set page(width: auto, height: auto, margin: 5pt)\n'
             '#set text(size: 20pt, fill: rgb("#edf6ff"))\n'+value+'\n',encoding='utf-8')
def main():
    create_sources()
    if not shutil.which('typst'):raise RuntimeError('Typst binary missing: use GitHub Actions')
    dest=ROOT/'assets/stat12_formulas';dest.mkdir(parents=True,exist_ok=True)
    for key in FORMULAS:
        src=ROOT/'typst/stat12'/f'{key}.typ';target=dest/f'{key}.svg'
        subprocess.run(['typst','compile','--format','svg',str(src),str(target)],check=True)
        if not target.is_file() or target.stat().st_size<150:raise RuntimeError(f'Empty SVG: {key}')
        if '<svg' not in target.read_text(encoding='utf-8')[:2000]:raise RuntimeError(f'Invalid SVG: {key}')
    print('STAT12_TYPST_PASS',len(FORMULAS))
if __name__=='__main__':main()
