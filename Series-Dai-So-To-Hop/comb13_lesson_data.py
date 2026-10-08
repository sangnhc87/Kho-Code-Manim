"""COMB13 V2: restrictions on adjacency and gap constructions.
Pure-Python: independent mathematical verification without Manim/Typst.
"""
from dataclasses import dataclass
from itertools import permutations, combinations
from collections import Counter
from math import factorial, comb
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
CHAPTER_LABELS={chapter:label for chapter,label,_ in json.loads((ROOT/'comb13_chapters.json').read_text(encoding='utf8'))}
FORMULAS=json.loads((ROOT/'comb13_formulas.json').read_text(encoding='utf8'))
@dataclass(frozen=True)
class Beat:
    section:str
    state:int
    heading:str
    lines:tuple[str,str,str]
    takeaway:str
    narration:str
    formula:str
    min_seconds:float
BEATS=tuple(Beat(b['section'],b['state'],b['heading'],tuple(b['lines']),b['takeaway'],b['narration'],b['formula'],float(b['min_seconds'])) for b in json.loads((ROOT/'comb13_beats.json').read_text(encoding='utf8')))
def adjacent(p,a,b):return abs(p.index(a)-p.index(b))==1
def on_circle_adjacent(p,a,b):
    n=len(p);return (p.index(a)-p.index(b))%n in (1,n-1)
def none_adjacent(p,pairs):return all(not adjacent(p,a,b) for a,b in pairs)
def distinct_gaps(m,k):
    return 0 if k>m+1 or k<0 else comb(m+1,k)
def nonconsecutive_positions(n,k):
    if k<0 or n<0 or n-k+1<k:return 0
    return comb(n-k+1,k)
def normalized_cycles(n):
    # Rotations identified: fix 0. Reflections remain different.
    for p in permutations(range(1,n)):
        yield (0,*p)
def validate():
    assert len(BEATS)==48 and len(CHAPTER_LABELS)==8
    assert Counter(b.section for b in BEATS)==dict.fromkeys(CHAPTER_LABELS,6)
    assert all(b.formula in FORMULAS for b in BEATS)
    assert min(len(b.narration.split()) for b in BEATS)>=38
    assert sum(b.min_seconds for b in BEATS)>1080
    p5=list(permutations(range(5)))
    assert sum(not adjacent(p,0,1) for p in p5)==72
    assert factorial(3)*comb(4,2)*factorial(2)==72
    p6=list(permutations(range(6)))
    ab=lambda p:adjacent(p,0,1)
    cd=lambda p:adjacent(p,2,3)
    bc=lambda p:adjacent(p,1,2)
    ac=lambda p:adjacent(p,0,2)
    assert sum(not ab(p) and not cd(p) for p in p6)==336
    assert sum(ab(p)!=cd(p) for p in p6)==288
    assert sum(not ab(p) and not bc(p) for p in p6)==288
    assert sum(not ab(p) and not bc(p) and not ac(p) for p in p6)==144
    assert 3*2**2*factorial(6)==8640
    assert 2**3*factorial(5)==960
    p8=list(permutations(range(8)))
    assert sum(none_adjacent(p,((0,1),(2,3),(4,5))) for p in p8)==17760
    assert factorial(8)-3*2*factorial(7)+3*4*factorial(6)-8*factorial(5)==17760
    assert sum(not on_circle_adjacent(p,0,1) for p in normalized_cycles(6))==72
    assert sum(all(not on_circle_adjacent(p,a,b) for a,b in ((0,1),(0,2),(1,2))) for p in normalized_cycles(6))==12
    assert nonconsecutive_positions(9,4)==15
    assert factorial(5)*comb(6,4)*factorial(4)==43200
    assert factorial(5)*comb(6,3)*factorial(3)==14400
    assert factorial(3)*comb(4,3)*factorial(3)==144
    return True
if __name__=='__main__':
    validate()
    print(f'COMB13 VALID beats={len(BEATS)} words={sum(len(b.narration.split()) for b in BEATS)} duration_min={sum(b.min_seconds for b in BEATS)/60:.2f}')
