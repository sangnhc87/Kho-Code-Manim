"""Mathematical source of truth for COMB20 (no Manim dependency)."""
from __future__ import annotations
from dataclasses import dataclass
from itertools import combinations
from math import comb
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
CHAPTERS = json.loads((ROOT/'comb20_chapters.json').read_text(encoding='utf-8'))
CHAPTER_LABELS = dict(CHAPTERS)
FORMULAS = json.loads((ROOT/'comb20_formulas.json').read_text(encoding='utf-8'))
DATA = json.loads((ROOT/'comb20_beats.json').read_text(encoding='utf-8'))

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




from math import comb, factorial
from fractions import Fraction

def row(n):
    if n<0: raise ValueError('n must be nonnegative')
    return tuple(comb(n,k) for k in range(n+1))

def ordinary(n):
    return sum(row(n))

def alternating(n):
    return sum((-1)**k*comb(n,k) for k in range(n+1))

def parity(n):
    return (sum(comb(n,k) for k in range(0,n+1,2)),
            sum(comb(n,k) for k in range(1,n+1,2)))

def falling(k,r):
    if r<0: raise ValueError('r must be nonnegative')
    if k<r:return 0
    out=1
    for j in range(r):out*=k-j
    return out

def weighted(n,r,a=1,b=1):
    if min(n,r)<0:raise ValueError('n,r must be nonnegative')
    return sum(falling(k,r)*comb(n,k)*b**k*a**(n-k) for k in range(n+1))

def power_weighted(n,p,a=1,b=1):
    if min(n,p)<0:raise ValueError('n,p must be nonnegative')
    return sum(k**p*comb(n,k)*b**k*a**(n-k) for k in range(n+1))

def reciprocal(n):
    return sum((Fraction(comb(n,k),k+1) for k in range(n+1)),Fraction())

def partial_alternating(n,r):
    if not (0<=r<=n):raise ValueError('requires 0<=r<=n')
    return sum((-1)**k*comb(n,k) for k in range(r+1))

def challenge_terms():
    return tuple((k,k*k*comb(6,k)*2**k*3**(6-k)) for k in range(7))

def validate():
    assert len(CHAPTERS)==8 and len(BEATS)==48 and len(FORMULAS)==48
    assert all([b.state for b in BEATS[i:i+6]]==list(range(6)) for i in range(0,48,6))
    assert all(len(b.lines)==3 and b.formula in FORMULAS for b in BEATS)
    assert all(len(b.narration.split())>=45 for b in BEATS)
    assert sum(b.min_seconds for b in BEATS)>=1200
    for n in range(1,12):
        assert ordinary(n)==2**n and alternating(n)==0
        assert parity(n)==(2**(n-1),2**(n-1))
        assert weighted(n,1)==n*2**(n-1)
        assert power_weighted(n,2)==n*(n+1)*2**(n-2)
        assert reciprocal(n)==Fraction(2**(n+1)-1,n+1)
        for r in range(n):assert partial_alternating(n,r)==(-1)**r*comb(n-1,r)
    assert sum(v for k,v in challenge_terms())==112500
    assert weighted(6,1,3,2)+weighted(6,2,3,2)==112500
    return True
if __name__=='__main__':print('COMB20_VALID',validate(), 'beats=',len(BEATS))
