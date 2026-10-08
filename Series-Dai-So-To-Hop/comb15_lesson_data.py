"""COMB15: forming natural numbers under digit restrictions; exact counting tests."""
from dataclasses import dataclass
from collections import Counter
from itertools import permutations,product
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
CHAPTERS=json.loads((ROOT/'comb15_chapters.json').read_text(encoding='utf-8'))
CHAPTER_LABELS={c[0]:c[1] for c in CHAPTERS}
FORMULAS=json.loads((ROOT/'comb15_formulas.json').read_text(encoding='utf-8'))
DATA=json.loads((ROOT/'comb15_beats.json').read_text(encoding='utf-8'))
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
BEATS=tuple(Beat(r['section'],r['state'],r['heading'],tuple(r['lines']),r['takeaway'],r['narration'],r['formula'],r['min_seconds']) for r in DATA)
def enumerate_numbers(symbols, length, distinct=True):
    digits=tuple(str(c) for c in symbols)
    paths=permutations(digits,length) if distinct else product(digits,repeat=length)
    return tuple(int(''.join(a)) for a in paths if a[0]!='0')
def mathematical_checks():
    x3=enumerate_numbers('012345',3)
    x3rep=enumerate_numbers('012345',3,False)
    assert len(x3)==100 and len(x3rep)==180
    p3=enumerate_numbers('01234',3)
    assert len(p3)==48 and sum(n%2==0 for n in p3)==30 and sum(n%2!=0 for n in p3)==18
    p4_07=enumerate_numbers('0123456',4)
    assert len(p4_07)==720 and sum(n%5==0 for n in p4_07)==220
    assert sum(n%10==0 for n in p4_07)==120
    assert sum(n%10==5 for n in p4_07)==100
    assert sum(n%3==0 for n in x3)==40
    assert sum(n>300 and n%2==0 for n in x3)==32
    p4=enumerate_numbers('012345',4)
    p4rep=enumerate_numbers('012345',4,False)
    assert len(p4)==300 and len(p4rep)==1080
    assert len(p4rep)-len(p4)==780
    divisible4=[n for n in p4 if n%4==0]
    assert len(divisible4)==72
    tails=Counter(f'{n:04d}'[-2:] for n in divisible4)
    assert dict(sorted(tails.items()))=={'04':12,'12':9,'20':12,'24':9,'32':9,'40':12,'52':9}
    valid=[n for n in p4 if n>3000 and n%15==0]
    assert len(valid)==24
    assert Counter(n//1000 for n in valid)=={3:12,4:8,5:4}
    assert Counter((n//1000,n%10) for n in valid)=={(3,0):8,(3,5):4,(4,0):4,(4,5):4,(5,0):4}
    return True
def validate():
    assert len(CHAPTERS)==8 and len(BEATS)==48
    assert Counter(b.section for b in BEATS)=={ch[0]:6 for ch in CHAPTERS}
    assert [b.state for b in BEATS]==list(range(6))*8
    assert all(b.formula in FORMULAS and len(b.lines)==3 for b in BEATS)
    assert min(len(b.narration.split()) for b in BEATS)>=43
    assert sum(b.min_seconds for b in BEATS)>=1152
    return mathematical_checks()
if __name__=='__main__':
    validate();print('COMB15_VALID',len(BEATS),len(CHAPTERS),sum(len(b.narration.split()) for b in BEATS))
