"""COMB12: Gộp khối, giao nhau và bao hàm–loại trừ."""
from __future__ import annotations
from dataclasses import dataclass
from itertools import permutations
from math import factorial
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
CHAPTER_LABELS = {chapter:label for chapter,label,_ in __import__('json').loads((ROOT/'comb12_chapters.json').read_text(encoding='utf-8'))}
FORMULAS = json.loads((ROOT/'comb12_formulas.json').read_text(encoding='utf-8'))
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
BEATS=tuple(Beat(b['section'],b['state'],b['heading'],tuple(b['lines']),b['takeaway'],b['narration'],b['formula'],float(b['min_seconds'])) for b in json.loads((ROOT/'comb12_beats.json').read_text(encoding='utf-8')))

def adjacent(p,x,y):
    return abs(p.index(x)-p.index(y))==1

def consecutive_group(p,items):
    positions=sorted(p.index(x) for x in items)
    return positions[-1]-positions[0]==len(items)-1

def enumerate_arrangements(n):
    return permutations(range(n))

def validate():
    from collections import Counter
    assert len(BEATS)==48
    assert Counter(b.section for b in BEATS)==dict.fromkeys(CHAPTER_LABELS,6)
    assert all(b.formula in FORMULAS for b in BEATS)
    assert all(len(b.narration.split())>=38 for b in BEATS)
    assert sum(b.min_seconds for b in BEATS)>1000
    p5=list(enumerate_arrangements(5))
    assert sum(adjacent(p,0,1) for p in p5)==48
    p6=list(enumerate_arrangements(6))
    assert len(p6)==720
    ab=lambda p:adjacent(p,0,1)
    cd=lambda p:adjacent(p,2,3)
    bc=lambda p:adjacent(p,1,2)
    assert sum(ab(p) for p in p6)==240
    assert sum(ab(p) and cd(p) for p in p6)==96
    assert sum(ab(p) or cd(p) for p in p6)==384
    assert sum(not ab(p) and not cd(p) for p in p6)==336
    assert sum(ab(p)!=cd(p) for p in p6)==288
    assert sum(ab(p) and not cd(p) for p in p6)==144
    assert sum(consecutive_group(p,(0,1,2)) for p in p6)==144
    assert sum(ab(p) and bc(p) for p in p6)==48
    assert sum(ab(p) and bc(p) and adjacent(p,0,2) for p in p6)==0
    assert sum(ab(p) and cd(p) and adjacent(p,4,5) for p in p6)==48
    assert sum(ab(p) and cd(p) and p.index(4)<p.index(5) for p in p6)==48
    p7=list(enumerate_arrangements(7))
    pairs=((0,1),(2,3),(4,5))
    assert sum(all(not adjacent(p,a,b) for a,b in pairs) for p in p7)==1968
    assert 5040-3*1440+3*480-192==1968
    return True

if __name__=='__main__':
    validate()
    print(f'COMB12 VALID beats={len(BEATS)} words={sum(len(x.narration.split()) for x in BEATS)} seconds={sum(x.min_seconds for x in BEATS)}')
