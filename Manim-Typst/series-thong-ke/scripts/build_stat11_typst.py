"""Generate and (in GitHub) compile eight visible Typst equations to SVG."""
from pathlib import Path
import shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
FORMULAS={
'ranges':'$ R_\"gốc\"=10-4=6 quad R_\"ghép\"=12-4=8 $',
'quartiles':'$ IQR=Q_3-Q_1 approx 2.41 $',
'r_vs_iqr':'$ R_\"ghép\"=8 quad IQR approx 2.41 $',
'two_samples':'$ R_A=R_B=8 quad IQR_A approx 2.41 < IQR_B=4 $',
'transform':'$ R(aX+b)=abs(a)R(X) quad IQR(aX+b)=abs(a)IQR(X) $',
'lost_info':'$ f_1=0 arrow R_\"ghép\"=12-6=6 $',
'mistakes':'$ R_\"ghép\"=U_\"cuối\"-L_\"đầu\" $',
'practice':'$ R_A=R_B=8 quad IQR_A approx 2.41 quad IQR_B=4 $',
}

def create_sources():
    dest=ROOT/'typst/stat11';dest.mkdir(parents=True,exist_ok=True)
    for name,formula in FORMULAS.items():
        (dest/f'{name}.typ').write_text(
            '#set page(width: auto, height: auto, margin: 5pt)\n'
            '#set text(size: 20pt, fill: rgb("#edf6ff"))\n'
            +formula+'\n',encoding='utf-8')
def main():
    create_sources()
    if not shutil.which('typst'):
        raise RuntimeError('Typst binary is missing: compile this in GitHub Actions')
    dest=ROOT/'assets/stat11_formulas';dest.mkdir(parents=True,exist_ok=True)
    for name in FORMULAS:
        src=ROOT/'typst/stat11'/f'{name}.typ';out=dest/f'{name}.svg'
        subprocess.run(['typst','compile','--format','svg',str(src),str(out)],check=True)
        if not out.is_file() or out.stat().st_size<150:
            raise RuntimeError(f'Invalid SVG compiled for {name}')
        if '<svg' not in out.read_text(encoding='utf-8')[:2000]:
            raise RuntimeError(f'SVG root not found for {name}')
    print('STAT11_TYPST_OK',len(FORMULAS),'SVG images')
if __name__=='__main__':main()
