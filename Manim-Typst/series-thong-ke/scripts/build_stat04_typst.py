"""Compile mathematically verified Typst formulas to SVG; fail early on syntax error."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1]
FORMULAS={
 'overview':r'$ Q_1 = 6 quad Q_2 = 7 quad Q_3 = 8 $',
 'halves':r'$ Q_2 = (x_20 + x_21) / 2 = 7 $',
 'positions':r'$ Q_1 = (x_10 + x_11) / 2 = 6 quad Q_3 = (x_30 + x_31) / 2 = 8 $',
 'cumulative':r'$ Q_1 = 6 quad Q_2 = 7 quad Q_3 = 8 $',
 'odd':r'$ Q_1 = 2.5 quad Q_2 = 5 quad Q_3 = 7.5 $',
 'outlier':r'$ Q_1 = 6 quad Q_2 = 7 quad Q_3 = 8 $',
 'iqr':r'$ IQR = Q_3 - Q_1 = 8 - 6 = 2 $',
 'exercise':r'$ (x + 7) / 2 = 6.5 quad x = 6 $',
}
def main():
    output=ROOT/'assets'/'stat04_formulas';output.mkdir(parents=True,exist_ok=True)
    docs=ROOT/'typst'/'stat04';docs.mkdir(parents=True,exist_ok=True)
    for key,expr in FORMULAS.items():
        source=docs/f'{key}.typ'
        source.write_text('#set page(width: auto, height: auto, margin: 5pt)\n'
                          '#set text(size: 22pt, fill: rgb("#ecf7ff"))\n'
                          +expr+'\n',encoding='utf-8')
        output_file=output/f'{key}.svg'
        subprocess.run(['typst','compile','--format','svg',str(source),str(output_file)],check=True)
        if output_file.stat().st_size<100:raise RuntimeError(f'Invalid SVG {key}')
    print('Compiled',len(FORMULAS),'STAT04 formula SVGs')
if __name__=='__main__':main()
