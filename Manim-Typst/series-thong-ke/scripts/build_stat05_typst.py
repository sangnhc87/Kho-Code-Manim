"""Compile eight STAT05 formula SVG assets. Fail explicitly on Typst errors."""
from pathlib import Path
import shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
FORMULAS={
 'range':r'$ R = 10 - 4 = 6 $',
 'five':r'$ "IQR" = Q_3 - Q_1 = 8 - 6 = 2 $',
 'construct':r'$ (4, 6, 7, 8, 10) $',
 'fences':r'$ 6 - 1.5 times 2 = 3 quad 8 + 1.5 times 2 = 11 $',
 'compare':r'$ "IQR"_A = 4 quad "IQR"_B = 8 $',
 'spread':r'$ R_A = R_B = 8 quad "IQR"_A = 8 quad "IQR"_B = 2 $',
 'conventions':r'$ Q_1 = Q_2 = Q_3 = 5 $',
 'exercise':r'$ R = 18 quad "IQR" = 4 quad Q_2 = 6 $',
}

def main():
    if shutil.which('typst') is None:raise RuntimeError('typst executable not on PATH')
    dest=ROOT/'assets'/'stat05_formulas';dest.mkdir(parents=True,exist_ok=True)
    source_dir=ROOT/'typst'/'stat05';source_dir.mkdir(parents=True,exist_ok=True)
    for key,value in FORMULAS.items():
        source=source_dir/f'{key}.typ'
        source.write_text('#set page(width: auto, height: auto, margin: 5pt)\n'
                          '#set text(size: 20pt, fill: rgb("#edf6ff"))\n'
                          +value+'\n',encoding='utf-8')
        svg=dest/f'{key}.svg'
        subprocess.run(['typst','compile','--format','svg',str(source),str(svg)],check=True)
        if not svg.is_file() or svg.stat().st_size<150:raise RuntimeError(f'Empty SVG: {svg}')
        if '<svg' not in svg.read_text(encoding='utf-8')[:1000]:raise RuntimeError(f'Not SVG: {svg}')
    print('STAT05_TYPST_OK',len(FORMULAS))
if __name__=='__main__':main()
