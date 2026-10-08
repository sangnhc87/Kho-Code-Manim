"""COMB17: Derive Newton's binomial formula by counting choices."""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from itertools import product
from math import comb
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
CHAPTERS=json.loads((ROOT/'comb17_chapters.json').read_text(encoding='utf8'))
CHAPTER_LABELS=dict(CHAPTERS)
FORMULAS=json.loads((ROOT/'comb17_formulas.json').read_text(encoding='utf8'))
DATA=json.loads((ROOT/'comb17_beats.json').read_text(encoding='utf8'))

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
BEATS=tuple(Beat(row['section'],row['state'],row['heading'],tuple(row['lines']),
    row['takeaway'],row['narration'],row['formula'],row['min_seconds']) for row in DATA)


def paths(n):
    """Independent binary-choice enumeration from the distributive rule."""
    return tuple(product('ab',repeat=n))


def grouped(n):
    return Counter(seq.count('b') for seq in paths(n))


def binomial_coefficients(n):
    return tuple(grouped(n)[k] for k in range(n+1))


def polynomial_mult(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out


def polynomial_power(constant,linear,n):
    result=[1]
    for _ in range(n):result=polynomial_mult(result,[constant,linear])
    return result


def product_capstone_coefficient(power):
    p=polynomial_mult(polynomial_power(1,1,4),polynomial_power(1,2,3))
    return p[power]


def coefficient_choose_splits(power):
    terms=[]
    for i in range(5):
        j=power-i
        if 0<=j<=3:terms.append((i,comb(4,i)*comb(3,j)*2**j))
    return terms


def validate():
    assert len(BEATS)==48
    assert len(CHAPTERS)==8
    assert len(FORMULAS)==48
    assert all(len(b.lines)==3 and b.formula in FORMULAS for b in BEATS)
    assert all(len(b.narration.split())>=40 for b in BEATS)
    assert [b.state for b in BEATS]==list(range(6))*8
    assert sum(b.min_seconds for b in BEATS)>=1150
    assert binomial_coefficients(2)==(1,2,1)
    assert binomial_coefficients(3)==(1,3,3,1)
    assert binomial_coefficients(4)==(1,4,6,4,1)
    assert binomial_coefficients(5)==(1,5,10,10,5,1)
    assert sum(binomial_coefficients(5))==32
    assert polynomial_power(-2,1,5)[3]==40
    assert polynomial_power(1,-1,5)[3]==-10
    assert polynomial_power(-1,2,6)[3]==-160
    assert polynomial_power(-1,2,6)[2]==60
    assert coefficient_choose_splits(3)==[(0,8),(1,48),(2,36),(3,4)]
    assert product_capstone_coefficient(3)==96
    return True

if __name__=='__main__':
    validate()
    print('COMB17_VALID 48 beats, 8 chapters, 96 capstone')
