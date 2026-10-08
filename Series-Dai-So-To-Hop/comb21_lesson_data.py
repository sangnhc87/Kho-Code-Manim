"""COMB21: exact mathematics and independently checkable lesson data.
No Manim/Typst dependency: all tests run on plain Python.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from math import comb, factorial
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
CHAPTERS=json.loads((ROOT/'comb21_chapters.json').read_text(encoding='utf-8'))
CHAPTER_LABELS=dict(CHAPTERS)
FORMULAS=json.loads((ROOT/'comb21_formulas.json').read_text(encoding='utf-8'))
DATA=json.loads((ROOT/'comb21_beats.json').read_text(encoding='utf-8'))

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

BEATS=tuple(Beat(x['section'],x['state'],x['heading'],tuple(x['lines']),
    x['takeaway'],x['narration'],x['formula'],x['min_seconds']) for x in DATA)

def convolve(a,b):
    """Exact Cauchy product for finite coefficient arrays."""
    if not a or not b:return []
    result=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):result[i+j]+=x*y
    return result

def geom_coeff(n,k):
    if n<0 or k<1:raise ValueError('n>=0 and k>=1 required')
    return comb(n+k-1,k-1)

def bound_two(n):
    """x1+...+x5=n, 0<=x1,x2<=2, all variables nonnegative."""
    if n<0:raise ValueError('n>=0 required')
    def coef(t):return comb(t+4,4) if t>=0 else 0
    return coef(n)-2*coef(n-3)+coef(n-6)

def bound_two_direct(n):
    if n<0:raise ValueError('n>=0 required')
    return sum(geom_coeff(n-a-b,3) for a in range(3) for b in range(3) if n>=a+b)

def tilings(n):
    if n<0:raise ValueError('n>=0')
    a,b=1,1
    for _ in range(n):a,b=b,a+b
    return a

def tiled_sequences(n):
    if n<0:raise ValueError('n>=0')
    if n==0:return [()]
    out=[]
    for step in (1,2):
        if n>=step:
            out.extend((step,)+tail for tail in tiled_sequences(n-step))
    return out

def onto(n,k):
    if n<0 or k<0:raise ValueError('nonnegative required')
    if k==0:return int(n==0)
    return sum((-1)**j*comb(k,j)*(k-j)**n for j in range(k+1))

def stirling2(n,k):
    if n<0 or k<0:raise ValueError('nonnegative required')
    return onto(n,k)//factorial(k) if k else int(n==0)

def exponential_product_coeff(n,k):
    """n! [x^n](e^x-1)^k, exact finite rational arithmetic."""
    if min(n,k)<0:raise ValueError('nonnegative required')
    coeff=[Fraction(0)]*(n+1);coeff[0]=Fraction(1)
    unit=[Fraction(0)]+[Fraction(1,factorial(j)) for j in range(1,n+1)]
    for _ in range(k):
        new=[Fraction(0)]*(n+1)
        for j,a in enumerate(coeff):
            for i in range(n+1-j):new[i+j]+=a*unit[i]
        coeff=new
    return int(coeff[n]*factorial(n))

def coin_ways(total, denominations=(1,2,3)):
    if total<0:raise ValueError('total>=0')
    if any(d<=0 for d in denominations):raise ValueError('positive denominations')
    dp=[0]*(total+1);dp[0]=1
    for d in denominations:
        for t in range(d,total+1):dp[t]+=dp[t-d]
    return dp[total]

def coin_ways_direct(total):
    if total<0:raise ValueError('total>=0')
    return sum(1 for x in range(total+1) for y in range(total//2+1)
               for z in range(total//3+1) if x+2*y+3*z==total)

def validate():
    assert len(CHAPTERS)==8 and len(BEATS)==48 and len(FORMULAS)==48
    assert len(set(x.formula for x in BEATS))==48
    assert list(CHAPTER_LABELS)==[BEATS[i].section for i in range(0,48,6)]
    for i,b in enumerate(BEATS):
        assert b.state==i%6 and b.section in CHAPTER_LABELS
        assert len(b.lines)==3 and b.formula in FORMULAS
        assert len(b.narration.split())>=38
    assert sum(x.min_seconds for x in BEATS)>=1200
    assert convolve([1,1,1],[1,0,1])==[1,1,2,1,1]
    assert geom_coeff(6,3)==28
    for n in range(31):assert bound_two(n)==bound_two_direct(n)
    for n in range(10):assert tilings(n)==len(tiled_sequences(n))
    for n in range(1,8):
        for k in range(1,5):assert onto(n,k)==exponential_product_coeff(n,k)
    assert onto(4,3)==36 and stirling2(4,2)==7
    assert coin_ways(12)==coin_ways_direct(12)==19
    assert bound_two(12)==600
    return True

if __name__=='__main__':print('COMB21_VALID',validate(),'words',sum(len(x.narration.split()) for x in BEATS))
