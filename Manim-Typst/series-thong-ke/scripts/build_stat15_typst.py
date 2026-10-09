"""Eight Typst formula SVGs; a compile failure stops the GitHub workflow."""
from pathlib import Path
import shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
FORMULAS={
 'bar': '$ 100/80=1.25 quad (100-75)/(80-75)=5 $',
 'scale': '$ Delta y = 56-40 = 16 $',
 'time': '$ (52-44)/(2024-2021)=8/3 $',
 'icons': '$ A=pi r^2 quad (sqrt(2)r)^2=2r^2 $',
 'rates': '$ 18/30=0.6 quad 24/80=0.3 $',
 'trend': '$ (54-60)/60=-0.1 quad (64-50)/50=0.28 $',
 'histogram': '$ h_i=f_i/(b_i-a_i) quad S_i=h_i(b_i-a_i)=f_i $',
 'detective': '$ 68-62=6 quad 68/62 approx 1.097 $',
}
def create_sources():
    path=ROOT/'typst/stat15';path.mkdir(parents=True,exist_ok=True)
    for k,v in FORMULAS.items():
        (path/(k+'.typ')).write_text('#set page(width: auto, height: auto, margin: 5pt)\n'
            '#set text(size: 20pt, fill: rgb("#edf6ff"))\n'+v+'\n',encoding='utf-8')

def main():
    create_sources()
    if not shutil.which('typst'):
        raise RuntimeError('Typst binary unavailable here; compile in GitHub Actions')
    dest=ROOT/'assets/stat15_formulas';dest.mkdir(parents=True,exist_ok=True)
    for name in FORMULAS:
        src=ROOT/'typst/stat15'/f'{name}.typ';out=dest/f'{name}.svg'
        subprocess.run(['typst','compile','--format','svg',str(src),str(out)],check=True)
        if not out.is_file() or out.stat().st_size<150 or '<svg' not in out.read_text(encoding='utf-8')[:2000]:
            raise RuntimeError(f'Missing or invalid Typst SVG: {name}')
    print('STAT15_TYPST_PASS',len(FORMULAS))
if __name__=='__main__':main()
