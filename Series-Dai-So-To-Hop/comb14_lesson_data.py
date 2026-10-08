"""COMB14 V2. Pure combinatorics and independently testable lesson metadata."""
from __future__ import annotations
from dataclasses import dataclass
from collections import Counter
from itertools import permutations, product, combinations
from math import factorial, comb, perm
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
BEAT_RECORDS=json.loads((ROOT/'comb14_beats.json').read_text(encoding='utf-8'))
CHAPTERS=json.loads((ROOT/'comb14_chapters.json').read_text(encoding='utf-8'))
CHAPTER_LABELS={x[0]:x[1] for x in CHAPTERS}
FORMULAS=json.loads((ROOT/'comb14_formulas.json').read_text(encoding='utf-8'))

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

BEATS=tuple(Beat(b['section'],b['state'],b['heading'],tuple(b['lines']),b['takeaway'],b['narration'],b['formula'],float(b['min_seconds'])) for b in BEAT_RECORDS)


def no_adjacent(bits): return all(bits[i:i+2]!=(1,1) for i in range(len(bits)-1))
def derangements(n): return sum(all(x!=i for i,x in enumerate(p)) for p in permutations(range(n)))
def team_captain_valid(team,captain): return (0 in team or 1 in team) and captain!=0

def mathematical_checks():
    # Exhaustive enumeration independent of displayed formulas.
    codes=list(product('ABC',repeat=4))
    assert len(codes)==81
    assert sum('A' in c for c in codes)==65
    assert sum(c.count('A')==1 for c in codes)==32
    teams=list(combinations(range(9),3))
    assert len(teams)==84
    assert sum(any(x>=5 for x in t) for t in teams)==74
    assert sum(sum(x>=5 for x in t)==1 for t in teams)==40
    assert sum(sum(x>=5 for x in t)==2 for t in teams)==30
    assert sum(sum(x>=5 for x in t)==3 for t in teams)==4
    p5=list(permutations(range(5)))
    assert sum(abs(p.index(0)-p.index(1))>1 for p in p5)==72
    p6=list(permutations(range(6)))
    assert sum(p[0]!=0 for p in p6)==600
    assert sum(p[0]!=0 and abs(p.index(0)-p.index(1))>1 for p in p6)==384
    pin_total=10**4
    assert pin_total-perm(10,4)==4960
    assert 9*1000-(9*9*8*7)==4464
    assert derangements(4)==9
    assert derangements(5)==44
    assert sum(sum(i==x for i,x in enumerate(p))==1 for p in permutations(range(4)))==8
    bs=list(product((0,1),repeat=6))
    assert len(bs)==64
    assert sum(no_adjacent(b) for b in bs)==21
    assert sum(not no_adjacent(b) for b in bs)==43
    team3=list(combinations(range(8),3))
    assert sum(0 in t or 1 in t for t in team3)==36
    assert sum((0 in t) != (1 in t) for t in team3)==30
    assert sum(0 in t and 1 in t for t in team3)==6
    results=[(t,cap) for t in combinations(range(8),4) for cap in t]
    assert len(results)==280
    assert sum(team_captain_valid(t,cap) for t,cap in results)==185
    assert sum(0 not in t and 1 not in t for t,cap in results)==60
    assert sum(cap==0 for t,cap in results)==35
    assert 280-60-35==comb(7,3)+6*(comb(7,3)-comb(5,3))==185
    return True


def validate():
    assert len(BEATS)==48 and len(CHAPTERS)==8
    assert Counter(b.section for b in BEATS)=={c[0]:6 for c in CHAPTERS}
    assert [b.state for b in BEATS]==list(range(6))*8
    assert all(b.formula in FORMULAS and len(b.lines)==3 for b in BEATS)
    assert min(len(b.narration.split()) for b in BEATS)>=48
    assert sum(b.min_seconds for b in BEATS)>1080
    assert mathematical_checks()
    return True
if __name__=='__main__':
    validate()
    print('COMB14 VALID:',len(BEATS),'beats,',sum(len(b.narration.split()) for b in BEATS),'words,',sum(b.min_seconds for b in BEATS),'seconds base')
