"""Generate editable .typ formula sources without requiring the Typst executable."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from int01.lesson import FORMULAS

def write():
    out=ROOT/'typst/int01';out.mkdir(parents=True,exist_ok=True)
    for key,expr in FORMULAS.items():
        (out/f'{key}.typ').write_text('#set page(width: auto, height: auto, margin: 2pt, fill: none)\n'
                 '#set text(size: 29pt, fill: rgb("#F1F5F9"))\n$'+expr+'$\n',encoding='utf8')
    print('INT01_TYPST_SOURCES_OK',len(FORMULAS))
if __name__=='__main__':write()
