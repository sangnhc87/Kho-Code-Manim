"""Mathematical source of truth for COMB19 (no Manim dependency)."""
from __future__ import annotations
from dataclasses import dataclass
from itertools import combinations
from math import comb
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
CHAPTERS = json.loads((ROOT/'comb19_chapters.json').read_text(encoding='utf-8'))
CHAPTER_LABELS = dict(CHAPTERS)
FORMULAS = json.loads((ROOT/'comb19_formulas.json').read_text(encoding='utf-8'))
DATA = json.loads((ROOT/'comb19_beats.json').read_text(encoding='utf-8'))

@dataclass(frozen=True)
class Beat:
    section: str
    state: int
    heading: str
    lines: tuple[str, str, str]
    takeaway: str
    narration: str
    formula: str
    min_seconds: float

BEATS = tuple(Beat(r['section'], r['state'], r['heading'], tuple(r['lines']),
                   r['takeaway'], r['narration'], r['formula'],r['min_seconds']) for r in DATA)



from itertools import combinations
from math import comb

def subset_masks(n: int):
    return tuple(tuple(i for i in range(n) if mask & (1<<i)) for mask in range(1<<n))

def size_counts(n: int):
    return tuple(sum(len(s)==k for s in subset_masks(n)) for k in range(n+1))

def distinguished(n: int):
    if n < 2: raise ValueError('n needs >=2')
    ss=subset_masks(n)
    return dict(contains_A=sum(0 in x for x in ss),
        excludes_A=sum(0 not in x for x in ss),
        A_not_B=sum(0 in x and 1 not in x for x in ss),
        exact_one=sum((0 in x)!=(1 in x) for x in ss),
        at_least_one=sum(0 in x or 1 in x for x in ss))

def parity_sizes(n: int):
    ss=subset_masks(n)
    return sum(len(x)%2==0 for x in ss),sum(len(x)%2==1 for x in ss)

def nonadjacent_subsets(n: int):
    return tuple(x for x in subset_masks(n) if all(b-a>1 for a,b in zip(x,x[1:])))

def nonadjacent_count(n: int):
    if n<0:raise ValueError('n must be nonnegative')
    p,q=1,2
    if n==0:return p
    if n==1:return q
    for i in range(2,n+1):p,q=q,p+q
    return q

def endpoint_breakdown(n=8):
    if n!=8:raise ValueError('This challenge has eight positions')
    valid=nonadjacent_subsets(n)
    left=sum(0 in x and n-1 not in x for x in valid)
    right=sum(n-1 in x and 0 not in x for x in valid)
    both=sum(0 in x and n-1 in x for x in valid)
    neither=sum(0 not in x and n-1 not in x for x in valid)
    return left,right,both,neither

def validate():
    assert len(CHAPTERS)==8 and len(BEATS)==48 and len(FORMULAS)==48
    assert all([b.state for b in BEATS[i:i+6]]==list(range(6)) for i in range(0,48,6))
    assert all(len(b.lines)==3 and b.formula in FORMULAS for b in BEATS)
    assert all(len(b.narration.split())>=50 for b in BEATS)
    assert sum(b.min_seconds for b in BEATS)+5.2>=1150
    assert size_counts(5)==(1,5,10,10,5,1)
    assert distinguished(5)==dict(contains_A=16,excludes_A=16,A_not_B=8,exact_one=16,at_least_one=24)
    assert parity_sizes(5)==(16,16) and parity_sizes(0)==(1,0)
    assert [nonadjacent_count(i) for i in range(9)]==[1,2,3,5,8,13,21,34,55]
    assert endpoint_breakdown()==(13,13,8,21)
    return True
if __name__=='__main__':
    print('COMB19_VALID',validate(),'chapters=8','beats=48','challenge=34')
